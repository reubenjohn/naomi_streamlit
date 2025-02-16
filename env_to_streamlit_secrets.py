import argparse
import logging
import os
from pathlib import Path


def write_secrets(toml_path: Path) -> None:
    toml_path.parent.mkdir(parents=True, exist_ok=True)
    with toml_path.open("w") as f:
        secret_content = os.environ.get("STREAMLIT_SECRETS_TOML", "")
        f.write(secret_content)
        logging.info(f"Secrets ({len(secret_content)} characters) written to {toml_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write Streamlit secrets to a TOML file.")
    parser.add_argument("toml_path", type=Path, help="The path to the TOML file.")
    args = parser.parse_args()
    write_secrets(args.toml_path)
