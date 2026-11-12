# Documentation tool entry points

For **v1.3.1**, run these from the repository root:

```bash
python3 tools/build_catalogue.py
python3 tools/build_diagrams_current.py
python3 tools/build_report_current.py
python3 tools/validate_spec.py
```

Builders need ReportLab, DejaVu fonts and Poppler; the validator uses Python's standard library and Poppler. No model weights, CUDA, CARLA or training environment is needed for these documentation checks.

The supplied approved logo is an immutable input, not a generated asset. Its SHA-256 is checked against `specs/release.json`.

Unversioned v1.1 builders and the v1.2/v1.3 scripts are retained as historical sources. They target superseded outputs, some depend on old local archive paths or additional PDF libraries, and their results do not represent current validation. `build_brand.py` builds historical vector trials; it does not generate the approved raster identity. Use the current commands above.

The CI definition in ci/validate-docs.yml is an inactive template. The publication credential lacks workflow scope; moving it into .github/workflows requires an authorized GitHub workflow write.
