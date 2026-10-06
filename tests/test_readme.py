from pathlib import Path


def test_readme_has_no_recieve_typo():
    readme = Path(__file__).resolve().parent.parent / "README.md"
    assert "recieve" not in readme.read_text()
