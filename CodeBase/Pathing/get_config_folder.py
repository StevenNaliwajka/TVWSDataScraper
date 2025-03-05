from pathlib import Path

from CodeBase.Pathing.get_project_root import get_project_root


def get_config_folder() -> Path:
    root = Path(get_project_root())
    config = root / 'Config'
    return config