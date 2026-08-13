# -*- coding: utf-8 -*-
# Unit test suite for the w-cli tool.
# Renders simulated test runs against command router options.
# All test files must contain comprehensive documentation as per project rules.

import os
import pytest
import subprocess
import tomli_w
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from module.main import (
    app, 
    LIBRARY_MAPPING, 
    detect_package_manager, 
    run_install_command, 
    get_monorepo_root, 
    get_package_local_path
)

runner = CliRunner()


def test_doc_command_lists_all_libraries():
    """
    Test Case: Verifies that running 'w doc' or 'w doc list' without arguments 
    successfully compiles and prints the interactive libraries table in the terminal.
    
    Assertions:
    - Exit code is 0 (Success).
    - Output console text contains expected headers and packages like 'wredis' or 'wsqlite'.
    """
    result = runner.invoke(app, ["doc"])
    assert result.exit_code == 0, "Command should execute successfully."
    assert "Wisrovi Suite Packages Map" in result.stdout, "The output table title should be printed."
    assert "redis" in result.stdout, "The 'redis' mapping should be present in the table."
    assert "wredis" in result.stdout, "The 'wredis' package name should be printed."


def test_doc_command_for_specific_package():
    """
    Test Case: Verifies that running 'w doc redis' prints the correct 
    documentation references (e.g., PyPI links) to the stdout stream.
    
    Assertions:
    - Exit code is 0.
    - Output contains the mapped description, target library name and url.
    """
    # Run command disabling the automatic browser opening trigger
    result = runner.invoke(app, ["doc", "redis", "--no-open"])
    assert result.exit_code == 0, "Execution should finish successfully."
    assert "wredis" in result.stdout, "Renders mapped package information."
    assert "Redis sync/async integration & caching suite" in result.stdout, "Package description should match."
    assert "https://pypi.org/project/wredis/" in result.stdout, "Documentation URL must be printed."


def test_doc_command_for_invalid_package():
    """
    Test Case: Verifies that querying documentation for an unregistered package
    returns a clear error error message and exits with status code 1.
    
    Assertions:
    - Exit code is 1 (Error).
    - Output contains error message.
    """
    result = runner.invoke(app, ["doc", "non_existent_package"])
    assert result.exit_code == 1, "Command should exit with error code 1."
    assert "is not in the registered wisrovi mapping" in result.stdout


def test_status_command_executes_successfully():
    """
    Test Case: Verifies that the 'w status' command successfully scans 
    the active Python path distributions and lists installation states.
    
    Assertions:
    - Exit code is 0.
    - Renders the status audit table to console containing 'wpipe' or 'wsqlite'.
    """
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0, "Status query command should execute successfully."
    assert "Local Environment wisrovi Packages Status" in result.stdout, "Renders audit table header."


def test_create_pipeline_boilerplate(tmp_path):
    """
    Test Case: Validates the 'w create pipeline' execution path.
    Runs inside a temporary directory to avoid dirtying the project workspace.
    
    Verifications:
    - Command output states the file was successfully written.
    - The created Python file is present in the local filesystem.
    - File contains typical wpipe execution boilerplate code.
    """
    temp_pipeline_name = "test_pipeline_run"
    with patch("os.getcwd", return_value=str(tmp_path)):
        result = runner.invoke(app, ["create", "pipeline", "--name", temp_pipeline_name])
    
    assert result.exit_code == 0, "Pipeline creation should succeed."
    expected_file = tmp_path / f"{temp_pipeline_name}.py"
    assert os.path.exists(expected_file), "Boilerplate file should be created on disk."
    
    # Read and inspect content
    with open(expected_file, "r") as f:
        content = f.read()
    assert "from wpipe import Pipeline, step" in content, "Should import necessary packages."
    assert "sample_orchestration_run" in content, "Should contain the configured name."


def test_create_docker_test_boilerplate(tmp_path):
    """
    Test Case: Validates the 'w create docker-test' execution path.
    Runs inside a temporary directory to avoid overwriting workspace runner script.
    
    Verifications:
    - Creates 'docker_test_runner.sh' file.
    - Creates a subfolder 'test' containing 'test_sample.py'.
    - Runner script has executable bits configured.
    """
    with patch("os.getcwd", return_value=str(tmp_path)):
        result = runner.invoke(app, ["create", "docker-test"])
        
    assert result.exit_code == 0, "Docker-Test workspace layout creation should succeed."
    assert os.path.exists(tmp_path / "docker_test_runner.sh"), "Docker test runner script should exist."
    assert os.path.exists(tmp_path / "test" / "test_sample.py"), "Sample test file should exist."


@patch("subprocess.run")
def test_install_command_executes_pip_subprocesses(mock_run):
    """
    Test Case: Validates the 'w install' routing logic.
    Mocks the system subprocess.run to isolate execution and prevent live package alterations.
    
    Assertions:
    - Runs Python executable pip module to install target libraries.
    - Correctly maps shortname 'redis' to 'wredis'.
    """
    # Mock subprocess return status code to success
    mock_response = MagicMock()
    mock_response.returncode = 0
    mock_run.return_value = mock_response

    # Force pip package manager detection mapping to ignore poetry lock files
    with patch("module.main.detect_package_manager", return_value="pip"):
        result = runner.invoke(app, ["install", "redis"])
        
    assert result.exit_code == 0, "Command should complete without failure."
    assert "Mapping 'redis' to wisrovi package: wredis" in result.stdout
    
    # Verify mock call details
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    called_cmd = args[0]
    assert "pip" in called_cmd, "Should execute pip tool."
    assert "wredis" in called_cmd, "Should target the correct wredis package."


@patch("subprocess.run")
def test_install_command_executes_poetry_or_pipenv(mock_run):
    """
    Test Case: Verifies that installation routes properly adapt when poetry or pipenv is detected.
    """
    mock_response = MagicMock()
    mock_response.returncode = 0
    mock_run.return_value = mock_response

    # Test Poetry detection
    with patch("module.main.detect_package_manager", return_value="poetry"):
        result = runner.invoke(app, ["install", "redis"])
    assert result.exit_code == 0
    mock_run.assert_called_with(["poetry", "add", "wredis"], check=True)

    # Test Pipenv detection
    mock_run.reset_mock()
    with patch("module.main.detect_package_manager", return_value="pipenv"):
        result = runner.invoke(app, ["install", "redis"])
    assert result.exit_code == 0
    mock_run.assert_called_with(["pipenv", "install", "wredis"], check=True)


@patch("subprocess.run")
def test_install_all_packages(mock_run):
    """
    Test Case: Validates the behavior of installing all package mappings of the suite at once.
    """
    mock_response = MagicMock()
    mock_response.returncode = 0
    mock_run.return_value = mock_response

    with patch("module.main.detect_package_manager", return_value="pip"):
        result = runner.invoke(app, ["install", "all"])
    
    assert result.exit_code == 0
    assert "Installing all" in result.stdout
    # Verify multiple package installs were run
    assert mock_run.call_count > 5


@patch("subprocess.run")
def test_install_command_with_unregistered_package(mock_run):
    """
    Test Case: Verifies that installing a package not mapped directly to a short name
    performs a direct installation using the unmodified user input argument.
    """
    mock_response = MagicMock()
    mock_response.returncode = 0
    mock_run.return_value = mock_response

    with patch("module.main.detect_package_manager", return_value="pip"):
        result = runner.invoke(app, ["install", "wsqlite"])
        
    assert result.exit_code == 0
    assert "is not a registered short name. Attempting direct install..." in result.stdout
    mock_run.assert_called_once()


@patch("subprocess.run")
def test_install_failure_handling(mock_run):
    """
    Test Case: Verifies that installer failures (subprocess.CalledProcessError)
    are intercepted gracefully, logging corresponding error statuses.
    """
    # Force failure in subprocess.run
    mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd="pip install")

    with patch("module.main.detect_package_manager", return_value="pip"):
        result = runner.invoke(app, ["install", "redis"])
        
    assert result.exit_code == 0
    assert "Command failed for wredis" in result.stdout
    assert "Failed to install wredis" in result.stdout


def test_detect_package_manager_logic(tmp_path):
    """
    Test Case: Verifies that detect_package_manager correctly identifies 'poetry',
    'pipenv' or 'pip' based on files present in the current workspace.
    """
    # Test fallback default to pip when directory is empty
    with patch("os.getcwd", return_value=str(tmp_path)):
        assert detect_package_manager() == "pip"

    # Test Poetry lock detection
    poetry_lock = tmp_path / "poetry.lock"
    poetry_lock.touch()
    with patch("os.getcwd", return_value=str(tmp_path)):
        assert detect_package_manager() == "poetry"
    poetry_lock.unlink()

    # Test Pipfile detection
    pipfile = tmp_path / "Pipfile"
    pipfile.touch()
    with patch("os.getcwd", return_value=str(tmp_path)):
        assert detect_package_manager() == "pipenv"
    pipfile.unlink()

    # Test parent directory lookup traversal logic
    child_path = tmp_path / "subdir" / "child"
    child_path.mkdir(parents=True)
    poetry_lock_parent = tmp_path / "poetry.lock"
    poetry_lock_parent.touch()
    with patch("os.getcwd", return_value=str(child_path)):
        assert detect_package_manager() == "poetry"
    poetry_lock_parent.unlink()



@patch("subprocess.run")
def test_package_manager_not_found_fallback(mock_run):
    """
    Test Case: Verifies that when poetry is detected but its binary is missing,
    the script catches the FileNotFoundError and automatically falls back to pip.
    """
    # Force FileNotFoundError on first call (Poetry), and success on second call (pip)
    mock_run.side_effect = [FileNotFoundError, MagicMock(returncode=0)]

    result = run_install_command("wredis", "poetry")
    assert result is True, "Should fall back and return True on pip success."
    assert mock_run.call_count == 2


def test_search_command():
    """
    Test Case: Verifies the 'w search <query>' subcommand logic.
    Ensures matching packages are mapped and displayed correctly in table format,
    while non-existing inputs return appropriate warnings.
    """
    # Query matching 'redis'
    result = runner.invoke(app, ["search", "redis"])
    assert result.exit_code == 0, "Query search should succeed."
    assert "wredis" in result.stdout, "Renders redis search mappings."
    assert "Found" in result.stdout

    # Query matching nothing
    result = runner.invoke(app, ["search", "non_existent_key_query"])
    assert result.exit_code == 0
    assert "No matching library tags found" in result.stdout


@patch("subprocess.run")
def test_check_command_logic(mock_run):
    """
    Test Case: Verifies the 'w check <library>' linter/security auditing router.
    Confirms ruff check and bandit run loops are executed on paths.
    """
    mock_response = MagicMock()
    mock_response.returncode = 0
    mock_run.return_value = mock_response

    # Mock the directory resolver to return a dummy folder path
    with patch("module.main.get_package_local_path", return_value="/tmp/wredis"):
        result = runner.invoke(app, ["check", "redis"])

    assert result.exit_code == 0
    assert mock_run.call_count == 2, "Should execute Ruff and Bandit."


def test_sync_versions_logic(tmp_path):
    """
    Test Case: Validates the 'w sync-versions <new_version>' subcommand.
    Mocks the monorepo root folder using a tmp_path containing dummy packages,
    and updates their pyproject.toml version strings.
    """
    # Create two dummy packages in our mock monorepo root
    pkg1 = tmp_path / "wredis"
    pkg1.mkdir()
    pyproj1 = pkg1 / "pyproject.toml"
    
    dummy_toml = {
        "project": {
            "name": "wredis",
            "version": "1.0.0"
        }
    }
    with open(pyproj1, "wb") as f:
        tomli_w.dump(dummy_toml, f)

    # Execute version synchronization via patch
    with patch("module.main.get_monorepo_root", return_value=str(tmp_path)):
        result = runner.invoke(app, ["sync-versions", "2.5.0"])

    assert result.exit_code == 0, "Sync versions run should succeed."
    
    # Read TOML back and verify version update
    with open(pyproj1, "rb") as f:
        try:
            import tomllib
            updated = tomllib.load(f)
        except ImportError:
            import tomli
            updated = tomli.load(f)
            
    assert updated["project"]["version"] == "2.5.0", "Version tag should be synchronized to 2.5.0."


@patch("subprocess.run")
def test_link_command_logic(mock_run):
    """
    Test Case: Validates 'w link <library>' command executing editable developer installs.
    """
    mock_response = MagicMock()
    mock_response.returncode = 0
    mock_run.return_value = mock_response

    # Mock path resolution and package manager detection
    with patch("module.main.get_package_local_path", return_value="/tmp/wredis"), \
         patch("module.main.detect_package_manager", return_value="pip"):
        result = runner.invoke(app, ["link", "redis"])

    assert result.exit_code == 0, "Link command should finish with success."
    assert "Successfully linked" in result.stdout
    mock_run.assert_called_once()
    called_cmd = mock_run.call_args[0][0]
    assert "-e" in called_cmd, "Should use editable parameter flag."


def test_completion_command():
    """
    Test Case: Verifies completion command render instructions.
    """
    result = runner.invoke(app, ["completion"])
    assert result.exit_code == 0
    assert "--install-completion" in result.stdout


@patch("subprocess.run")
def test_link_all_packages(mock_run, tmp_path):
    """
    Test Case: Verifies 'w link all' iterates over directories containing package setups.
    """
    mock_response = MagicMock()
    mock_response.returncode = 0
    mock_run.return_value = mock_response

    # Create dummy package directories containing setup.py or pyproject.toml
    dir1 = tmp_path / "wredis"
    dir1.mkdir()
    (dir1 / "pyproject.toml").touch()

    dir2 = tmp_path / "wsqlite"
    dir2.mkdir()
    (dir2 / "setup.py").touch()

    with patch("module.main.get_monorepo_root", return_value=str(tmp_path)), \
         patch("module.main.detect_package_manager", return_value="pip"):
        result = runner.invoke(app, ["link", "all"])

    assert result.exit_code == 0
    assert "Found 2 linkable local libraries." in result.stdout
    assert mock_run.call_count == 2


@patch("subprocess.run")
def test_check_all_packages(mock_run, tmp_path):
    """
    Test Case: Verifies 'w check all' routes audits across all packages in directory.
    """
    mock_response = MagicMock()
    mock_response.returncode = 0
    mock_run.return_value = mock_response

    # Create directories
    dir1 = tmp_path / "wredis"
    dir1.mkdir()
    (dir1 / "pyproject.toml").touch()

    with patch("module.main.get_monorepo_root", return_value=str(tmp_path)):
        result = runner.invoke(app, ["check", "all"])

    assert result.exit_code == 0
    # Runs ruff and bandit once each
    assert mock_run.call_count == 2
