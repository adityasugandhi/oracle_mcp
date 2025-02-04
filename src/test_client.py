import asyncio
import json
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('test_client')

# Load environment variables
load_dotenv()

async def test_query():
    """Test a simple query execution"""
    # Using a simple, safe test query
    query = "SELECT 1 as TEST_COLUMN FROM DUAL"
    
    message = {
        "type": "tool_call",
        "tool": "execute_query",
        "arguments": {
            "query": query
        }
    }
    
    logger.info(f"Sending test query...")
    print(json.dumps(message))

async def main():
    """Main test function"""
    logger.info("Starting test client...")
    
    try:
        await test_query()
    except Exception as e:
        logger.error(f"Error in test: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())