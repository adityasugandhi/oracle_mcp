import os

import pytest
from dotenv import load_dotenv

# Load environment variables for tests
load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment variables if not present"""
    if "ORACLE_USER" not in os.environ:
        os.environ["ORACLE_USER"] = "test_user"
    if "ORACLE_PASSWORD" not in os.environ:
        os.environ["ORACLE_PASSWORD"] = "test_password"
    if "ORACLE_DSN" not in os.environ:
        os.environ["ORACLE_DSN"] = "localhost:1521/?sid=test"


@pytest.fixture
def test_query():
    """Return a simple test query"""
    return "SELECT 1 as TEST_COLUMN FROM DUAL"


@pytest.fixture
def mock_db_response():
    """Return a mock database response"""
    return [{"TEST_COLUMN": 1}]
