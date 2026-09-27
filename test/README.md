# 🧪 Test Suite (`test/`)

> **Proyecto:** `w-cli` — Wisrovi Libraries Suite Central CLI Manager  
> **Autor:** [William Steve Rodriguez Villamizar (Wisrovi)](https://wisrovi.dev)

---

## 📌 Propósito y Cobertura

Este directorio contiene las pruebas automatizadas (`pytest`) para validar los comandos, analizadores de argumentos, resolución de paquetes y despacho de subprocesos del CLI unificado `w`.

### Pruebas Principales:
* **[`test_cli.py`](test_cli.py)**: Suite completa de pruebas unitarias y de integración para la CLI:
  - Detección automática del gestor de paquetes (`pip`, `poetry`, `pipenv`).
  - Mapeo de short-names hacia paquetes oficiales y MCPs (`pipe` ➔ `wpipe`, `yolo-mcp` ➔ `wyoloservice-mcp`, etc.).
  - Comandos de auditoría (`w status`, `w check`, `w search`).
  - Sincronización de versiones en `pyproject.toml` (`w sync-versions`).
  - Scaffolding de pipelines DAG (`w create pipeline`).

---

## 🚀 Ejecución de Pruebas

```bash
# Ejecutar todas las pruebas con pytest
pytest -v test/

# Ejecutar con reporte de cobertura de código
pytest --cov=module --cov-report=term-missing
```

---

[⬅️ Volver al README Principal](../README.md)
