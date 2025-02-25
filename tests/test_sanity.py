from naomi_streamlit.sanity import sanity_check
import pytest


def test_entity_creation():
    with pytest.raises(ValueError, match="Sanity check"):
        sanity_check()
