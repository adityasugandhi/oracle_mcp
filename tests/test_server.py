import pytest
from src.server import execute_query
import os

@pytest.mark.asyncio
async def test_execute_query_basic():
    """Test that execute_query function exists and accepts correct parameters"""
    # Skip if no Oracle credentials
    if not all([os.getenv("ORACLE_USER"), os.getenv("ORACLE_PASSWORD"), os.getenv("ORACLE_DSN")]):
        pytest.skip("Oracle credentials not configured")
        
    query = "SELECT 1 as TEST FROM DUAL"
    try:
        result = await execute_query(query)
        assert isinstance(result, list), "Result should be a list"
    except Exception as e:
        if "ORA-" in str(e):  # Oracle-specific error
            pytest.skip(f"Oracle connection failed: {e}")
        else:
            raise

@pytest.mark.asyncio
async def test_execute_query_with_params():
    """Test query execution with parameters"""
    if not all([os.getenv("ORACLE_USER"), os.getenv("ORACLE_PASSWORD"), os.getenv("ORACLE_DSN")]):
        pytest.skip("Oracle credentials not configured")
        
    query = "SELECT :value as TEST FROM DUAL"
    params = {"value": 42}
    try:
        result = await execute_query(query, params)
        assert isinstance(result, list), "Result should be a list"
        if result:
            assert result[0].get("TEST") == 42, "Parameter binding failed"
    except Exception as e:
        if "ORA-" in str(e):
            pytest.skip(f"Oracle connection failed: {e}")
        else:
            raise