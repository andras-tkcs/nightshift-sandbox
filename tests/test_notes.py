from pathlib import Path


def test_notes_contains_second_run():
    notes = Path(__file__).resolve().parent.parent / "NOTES.md"
    assert "second run" in notes.read_text().splitlines()
