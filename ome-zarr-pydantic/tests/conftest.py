import pytest
from pathlib import Path


@pytest.fixture
def testdata_path():
    return Path(__file__).parent / "data"