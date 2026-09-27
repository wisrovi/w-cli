# 📦 Module (`module/`) — Central CLI Engine

> **Proyecto:** `w-cli` — Wisrovi Libraries Suite Central CLI Manager  
> **Autor:** [William Steve Rodriguez Villamizar (Wisrovi)](https://wisrovi.dev)

---

## 📌 Arquitectura del Módulo

El directorio `module/` alberga la lógica de despacho, formateo de consola con `rich`, parseo con `typer` y mapeos canónicos de la suite:

* **[`main.py`](main.py)**: Punto de entrada principal (`w = module.main:app`). Contiene:
  - `LIBRARY_MAPPING`: Mapeo exhaustivo de los 37 componentes (23 PyPI + 14 en desarrollo).
  - `detect_package_manager()`: Detector dinámico de `poetry`, `pipenv` o `pip`.
  - Subcomandos `install`, `doc`, `search`, `status`, `link`, `check`, `sync-versions`, `create`.
* **`submodule/`**: Extensiones internas de apoyo para helpers de inspección.

---

[⬅️ Volver al README Principal](../README.md)
