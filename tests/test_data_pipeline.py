from pathlib import Path


def test_project_structure():
    project_root = Path(__file__).resolve().parents[1]

    assert (project_root / "src").exists()
    assert (project_root / "mage").exists()
    assert (project_root / "README.md").exists()


def test_cleaning_script_exists():
    project_root = Path(__file__).resolve().parents[1]

    assert (project_root / "src" / "clean_data.py").exists()


def test_validation_script_exists():
    project_root = Path(__file__).resolve().parents[1]

    assert (project_root / "src" / "validate_data.py").exists()