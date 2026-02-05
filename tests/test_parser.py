from vcds_scan_analyzer import parse_scan_text


SAMPLE_LOG = """
Address 01: Engine
Part No SW: 1K0 906 032
Component: 2.0l R4/4V TFSI
No fault code found.

Address 03: ABS Brakes
Part No SW: 1K0 907 379
Component: ESP MK60EC1
Faults Found:
00300 - ABS Wheel Speed Sensor; Front Left (G47)
012 - Electrical Fault in Circuit
00290 - ABS Wheel Speed Sensor; Rear Left (G46)
011 - Open Circuit
"""


def test_parse_ecu_headers():
    report = parse_scan_text(SAMPLE_LOG)
    assert len(report.ecus) == 2
    assert report.ecus[0].address == "01"
    assert report.ecus[0].name == "Engine"
    assert report.ecus[1].address == "03"
    assert report.ecus[1].name == "ABS Brakes"


def test_parse_dtcs_with_details():
    report = parse_scan_text(SAMPLE_LOG)
    abs_module = report.ecus[1]
    assert len(abs_module.dtcs) == 2
    assert abs_module.dtcs[0].code == "00300"
    assert abs_module.dtcs[0].detail == "012 - Electrical Fault in Circuit"
    assert abs_module.dtcs[1].code == "00290"
    assert abs_module.dtcs[1].detail == "011 - Open Circuit"
