from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
import re


ECU_HEADER_RE = re.compile(r"^Address\s+(\S+):\s*(.+)$")
DTC_RE = re.compile(r"^([0-9A-F]{5})\s*-\s*(.+)$")


@dataclass
class DTC:
    code: str
    description: str
    detail: str | None = None


@dataclass
class ECU:
    address: str
    name: str
    dtcs: list[DTC] = field(default_factory=list)


@dataclass
class ScanReport:
    ecus: list[ECU] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "ecus": [
                {
                    "address": ecu.address,
                    "name": ecu.name,
                    "dtcs": [
                        {
                            "code": dtc.code,
                            "description": dtc.description,
                            "detail": dtc.detail,
                        }
                        for dtc in ecu.dtcs
                    ],
                }
                for ecu in self.ecus
            ]
        }


def _iter_lines(text: str | Iterable[str]) -> Iterable[str]:
    if isinstance(text, str):
        yield from text.splitlines()
    else:
        yield from text


def parse_scan_text(text: str | Iterable[str]) -> ScanReport:
    current_ecu: ECU | None = None
    report = ScanReport()
    expecting_detail = False

    for raw_line in _iter_lines(text):
        line = raw_line.rstrip()
        if not line:
            continue

        header_match = ECU_HEADER_RE.match(line)
        if header_match:
            current_ecu = ECU(address=header_match.group(1), name=header_match.group(2))
            report.ecus.append(current_ecu)
            expecting_detail = False
            continue

        if current_ecu is None:
            continue

        dtc_match = DTC_RE.match(line)
        if dtc_match:
            current_ecu.dtcs.append(
                DTC(code=dtc_match.group(1), description=dtc_match.group(2).strip())
            )
            expecting_detail = True
            continue

        if expecting_detail and current_ecu.dtcs:
            if re.match(r"^[0-9]{3}\s*-", line):
                current_ecu.dtcs[-1].detail = line.strip()
                expecting_detail = False
            elif line.startswith("Readiness"):
                expecting_detail = False

    return report


def parse_scan_file(path: str | Path) -> ScanReport:
    content = Path(path).read_text(encoding="utf-8", errors="ignore")
    return parse_scan_text(content)
