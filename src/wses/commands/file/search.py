import os
import sys
from pathlib import Path


def fast_search(
    target_filename, target_dir: Path | str = Path.home(), full_name: bool = False
):
    # os.scandir returns an iterator that points directly to system memory
    for entry in os.scandir(target_dir):
        if not entry.name.startswith(".") and not entry.name == "Library":
            condition = (
                target_filename == entry.name
                if full_name
                else target_filename in entry.name
            )
            if condition:
                yield Path(entry.path)
            elif entry.is_dir(follow_symlinks=False):
                # Recurse into subdirectories
                try:
                    yield from fast_search(
                        target_filename, target_dir=entry.path, full_name=full_name
                    )
                except PermissionError:
                    continue


def find_file(
    target_filename, target_dir: Path | str = Path.home(), full_name: bool = False
):
    options = [p for p in fast_search(target_filename, target_dir, full_name)]
    if len(options) == 1:
        choice = options[0]
    elif len(options) > 1:
        print(f"Multiple options found: {options}. Make a selection:")
        for i, option in enumerate(options):
            print(f"\t{i + 1}. {option}")
        choice = input("\tSelect an option: ")
    else:
        print(f"No files match your search criteria: {target_filename}")
        return None
        # sys.exit(1)
    return Path(choice)
