from pathlib import Path
import sys


def resource_path(relative_path: str) -> str:

    if hasattr(sys, "_MEIPASS"):

        base_path = Path(sys._MEIPASS)

    else:

        base_path = Path(__file__).resolve().parent.parent

    return str(
        base_path / relative_path
    )