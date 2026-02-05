# vcds-scan-analyzer

Paprastas VCDS Auto-Scan TXT failų parseris, kuris ištraukia ECU modulius ir DTC klaidas.

## Struktūra

```
src/vcds_scan_analyzer/
tests/
README.md
```

## Naudojimas

```python
from vcds_scan_analyzer import parse_scan_file

report = parse_scan_file("autoscan.txt")
print(report.as_dict())
```

## Paleidimas

```bash
pytest
```
