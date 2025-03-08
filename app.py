import argparse
import logging
from dotenv import load_dotenv

from naomi_core.db.core import initialize_db
from naomi_streamlit.home import run


def parse_args():
    parser = argparse.ArgumentParser(description="Streamlit app for managing message trees.")
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()

    logging.basicConfig(
        level=args.log_level.upper(), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Initialize database
    initialize_db()

    run()


if __name__ == "__main__":
    main()
