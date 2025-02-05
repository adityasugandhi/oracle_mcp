import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Sequence

import oracledb
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import EmbeddedResource, Resource, TextContent, Tool

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("oracle_mcp")

# Initialize server
server = Server("oracle-query")

# Load environment variables
load_dotenv()

# Configuration
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE")  # Can be SID or SERVICE_NAME

if not all([ORACLE_USER, ORACLE_PASSWORD, ORACLE_SERVICE]):
    raise ValueError("Oracle credentials not found in environment variables")


# Create the connection string using the host, port, and service name
# Example: "localhost:1521/ORCLPDB1" or "localhost:1521:ORCL" for SID
def get_connection_string():
    if "/" in ORACLE_SERVICE:  # If using service name
        return f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"
    else:  # If using SID
        return f"{ORACLE_HOST}:{ORACLE_PORT}:{ORACLE_SERVICE}"


async def execute_query(query: str, params: dict = None) -> List[Dict]:
    """Execute a query and return results"""
    try:
        # Create thin connection
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=get_connection_string(),
            config_dir=None,  # Disable tnsnames.ora lookup
        )

        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Get column names
        columns = [col[0] for col in cursor.description] if cursor.description else []

        # Fetch results
        results = []
        rows = cursor.fetchall()
        for row in rows:
            result_dict = {}
            for i, column in enumerate(columns):
                value = row[i]
                # Convert special types to strings for JSON serialization
                if hasattr(value, "isoformat"):  # For dates/timestamps
                    value = value.isoformat()
                result_dict[column] = value
            results.append(result_dict)

        return results

    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available database query tools"""
    return [
        Tool(
            name="execute_query",
            description="Execute a SQL query on the Oracle database",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute",
                    }
                },
                "required": ["query"],
            },
        )
    ]


@server.call_tool()
async def call_tool(
    name: str, arguments: Any
) -> Sequence[TextContent | EmbeddedResource]:
    """Handle tool calls for database operations"""
    logger.debug(f"Tool call received: {name} with arguments {arguments}")

    if name == "execute_query":
        if not isinstance(arguments, dict):
            raise ValueError("Invalid arguments")

        query = arguments.get("query")
        if not query:
            raise ValueError("Query is required")

        try:
            results = await execute_query(query)
            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return [TextContent(type="text", text=f"Error executing query: {str(e)}")]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the server"""
    from mcp.server.stdio import stdio_server

    logger.info("Starting Oracle MCP server...")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
