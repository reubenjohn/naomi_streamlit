#!/usr/bin/env python3
"""
Development mode toggle script.

This script helps switch between development and production modes:
- Development mode: Uses local naomi_core via symlink
- Production mode: Uses the naomi_core package from git

Usage:
    python dev_mode.py on   # Enable development mode
    python dev_mode.py off  # Disable development mode
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.absolute()
NAOMI_CORE_PATH = Path("../naomi_core/naomi_core")
SYMLINK_PATH = PROJECT_ROOT / "naomi_core"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
PYPROJECT_BACKUP = PROJECT_ROOT / "pyproject.toml.prod"


def enable_dev_mode():
    """Enable development mode with local naomi_core."""
    print("Enabling development mode...")

    # Back up production pyproject.toml if not already done
    if not PYPROJECT_BACKUP.exists():
        shutil.copy(PYPROJECT_PATH, PYPROJECT_BACKUP)
        print(f"Backed up {PYPROJECT_PATH} to {PYPROJECT_BACKUP}")

    # Create symlink if it doesn't exist
    if not SYMLINK_PATH.exists():
        os.symlink(NAOMI_CORE_PATH, SYMLINK_PATH)
        print(f"Created symlink from {NAOMI_CORE_PATH} to {SYMLINK_PATH}")

    # Modify pyproject.toml to include the symlinked directory
    with open(PYPROJECT_PATH, "r") as f:
        content = f.read()

    if 'packages = [{include = "naomi_streamlit"}]' in content:
        content = content.replace(
            'packages = [{include = "naomi_streamlit"}]',
            'packages = [{include = "naomi_streamlit"}, {include = "naomi_core"}]',
        )
        with open(PYPROJECT_PATH, "w") as f:
            f.write(content)
        print("Updated pyproject.toml to include naomi_core package")

    # Update poetry dependencies
    subprocess.run(["poetry", "install"], cwd=PROJECT_ROOT)
    print("Development mode enabled. Restart your Streamlit app.")


def disable_dev_mode():
    """Disable development mode and revert to production settings."""
    print("Disabling development mode...")

    # Remove symlink if it exists
    if SYMLINK_PATH.exists():
        os.unlink(SYMLINK_PATH)
        print(f"Removed symlink at {SYMLINK_PATH}")

    # Restore original pyproject.toml
    if PYPROJECT_BACKUP.exists():
        shutil.copy(PYPROJECT_BACKUP, PYPROJECT_PATH)
        print(f"Restored {PYPROJECT_PATH} from {PYPROJECT_BACKUP}")

    # Update poetry dependencies
    subprocess.run(["poetry", "install"], cwd=PROJECT_ROOT)
    print("Development mode disabled. Restart your Streamlit app.")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["on", "off"]:
        print("Usage: python dev_mode.py [on|off]")
        sys.exit(1)

    if sys.argv[1] == "on":
        enable_dev_mode()
    else:
        disable_dev_mode()
