from pathlib import Path


def test_q2_file_contains_line():
    path = Path(__file__).resolve().parent.parent / "Q2.md"
    assert path.exists()
    assert "queue two" in path.read_text().splitlines()
