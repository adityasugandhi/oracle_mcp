import logging
import os
import oracledb
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('oracle_mcp')

# Load env variables
load_dotenv()

def test_oracle_connection():
    try:
        user = os.getenv("ORACLE_USER")
        password = os.getenv("ORACLE_PASSWORD")
        dsn = os.getenv("ORACLE_DSN")
        
        logger.debug(f"Attempting connection with DSN: {dsn}")
        
        connection = oracledb.connect(
            user=user,
            password=password,
            dsn=dsn
        )
        
        logger.debug("Connection successful")
        cursor = connection.cursor()
        cursor.execute("SELECT SYSDATE FROM DUAL")
        result = cursor.fetchone()
        logger.debug(f"Test query result: {result}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    test_oracle_connection()