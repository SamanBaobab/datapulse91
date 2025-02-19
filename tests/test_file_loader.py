# Tester detect_file_type_path du file_loader
import pytest

from datapulse91.processing.file_loader import detect_file_type_path

@pytest.mark.parametrize("filename, expected_type", [
    ("test.json", "json"),
    ("test.csv", "csv"),
    ("test.txt", "txt"),
    ("test.unknown", None),
])
def test_detect_file_type_path(filename, expected_type):
    assert detect_file_type_path(filename) == expected_type




