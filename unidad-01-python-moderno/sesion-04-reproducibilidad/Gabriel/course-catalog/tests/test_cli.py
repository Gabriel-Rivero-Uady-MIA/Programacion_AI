import subprocess
import sys
from pathlib import Path


def test_missing_catalog_returns_1_and_empty_stdout(tmp_path: Path) -> None:
    missing_catalog = tmp_path / "missing.json"

    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "python",
            "--catalog",
            str(missing_catalog),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert result.stdout == ""
