from pathlib import Path


def test_notes_contains_line():
    notes = Path(__file__).resolve().parent.parent / "NOTES.md"
    assert "second run" in notes.read_text().splitlines()
