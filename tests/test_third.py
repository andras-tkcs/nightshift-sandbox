from pathlib import Path


def test_third_md_has_line():
    text = (Path(__file__).resolve().parent.parent / "THIRD.md").read_text()
    assert "third run" in text.splitlines()
