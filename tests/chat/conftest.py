from typing import Iterator
from unittest.mock import patch
import pytest


@pytest.fixture
def mock_llm_client():
    with patch("naomi_core.assistant.agent.llm_client") as mock:
        yield mock


def pass_thru_process_llm_response(chunks: Iterator[str]) -> Iterator[str]:
    return chunks


@pytest.fixture(scope="function", autouse=True)
def patch_process_llm_response():
    with patch(
        "naomi_core.assistant.persistence.process_llm_response",
        side_effect=pass_thru_process_llm_response,
    ):
        yield
