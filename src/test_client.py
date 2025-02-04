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
    query = "SELECT 1 as TEST_COLUMN FROM DUAL"
    
    message = {
        "type": "tool_call",
        "tool": "execute_query",
        "arguments": {
            "query": query
        }
    }
    
    print(f"Sending message: {json.dumps(message)}")
    print(json.dumps(message))
    
    # In a real implementation, you would:
    # 1. Read the response
    # 2. Parse the JSON
    # 3. Handle any errors
    # 4. Process the results

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