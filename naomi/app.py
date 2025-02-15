import argparse
import logging
from dotenv import load_dotenv
import streamlit as st

from naomi.Hello import run


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
    st.set_page_config(page_title="AI Chat App", page_icon="🤖")
    args = parse_args()

    logging.basicConfig(
        level=args.log_level.upper(), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    run()


if __name__ == "__main__":
    main()
