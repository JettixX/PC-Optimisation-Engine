import json
import subprocess
from pathlib import Path

from PCOptimisationEngine.src.models.components import (
    CPU,
    GPU,
    MOTHERBOARD,
    RAM,
    STORAGE,
    PSU,
    CASE,
    COOLER,
)


REPO_URL = "https://github.com/buildcores/buildcores-open-db"


def sync_opendb_repo(target_dir: Path) -> None:
    """Clone OpenDB if absent, otherwise update the existing clone."""

    if not target_dir.exists():
        print(f"Cloning BuildCores OpenDB into {target_dir}...")
        subprocess.run(
            ["git", "clone", REPO_URL, str(target_dir)],
            check=True,
        )
        return

    git_dir = target_dir / ".git"

    if not git_dir.exists():
        raise RuntimeError(
            f"{target_dir} exists but is not a Git repository."
        )

    print("Updating BuildCores OpenDB...")
    subprocess.run(
        ["git", "-C", str(target_dir), "pull"],
        check=True,
    )


def load_category(
    repo_dir: Path,
    folder_name: str,
    dataclass_cls,
) -> list:
    """Load all JSON records in an OpenDB category."""

    target_folder = repo_dir / "open-db" / folder_name

    if not target_folder.exists():
        raise FileNotFoundError(
            f"OpenDB category not found: {target_folder}"
        )

    items = []

    for json_file in target_folder.glob("*.json"):
        try:
            with json_file.open("r", encoding="utf-8") as file:
                raw_data = json.load(file)

            item = dataclass_cls.from_opendb(raw_data)
            items.append(item)

        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
            print(
                f"Warning: could not parse "
                f"{json_file.name}: {exc}"
            )

    return items


def load_inventory(repo_dir: Path) -> dict:
    """Load the component categories used by the project."""

    return {
        "CPUs": load_category(
            repo_dir, "CPU", CPU
        ),
        "Motherboards": load_category(
            repo_dir, "Motherboard", MOTHERBOARD
        ),
        "GPUs": load_category(
            repo_dir, "GPU", GPU
        ),
        "RAM": load_category(
            repo_dir, "RAM", RAM
        ),
        "Storage": load_category(
            repo_dir, "Storage", STORAGE
        ),
        "PSUs": load_category(
            repo_dir, "PSU", PSU
        ),
        "Cases": load_category(
            repo_dir, "PCCase", CASE
        ),
        "Coolers": load_category(
            repo_dir, "CPUCooler", COOLER
        ),
    }