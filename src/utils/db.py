import oracledb
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger('oracle_mcp')

class DatabaseConnection:
    def __init__(self):
        self.user = os.getenv("ORACLE_USER")
        self.password = os.getenv("ORACLE_PASSWORD")
        self.dsn = os.getenv("ORACLE_DSN")
        
        if not all([self.user, self.password, self.dsn]):
            raise ValueError("Oracle credentials not found in environment variables")

    async def execute_query(self, query: str, params: Optional[dict] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results as a list of dictionaries"""
        try:
            connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
            )
            
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Get column names
            columns = [col[0] for col in cursor.description]
            
            # Fetch results and convert to list of dictionaries
            results = []
            for row in cursor.fetchall():
                result_dict = dict(zip(columns, row))
                # Convert Oracle specific types to JSON serializable formats
                for key, value in result_dict.items():
                    if isinstance(value, datetime):
                        result_dict[key] = value.isoformat()
                results.append(result_dict)
                
            return results
            
        except oracledb.Error as e:
            logger.error(f"Oracle DB error: {str(e)}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    async def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Get detailed information about a table"""
        query = """
        SELECT column_name, data_type, data_length, nullable, data_precision, data_scale
        FROM all_tab_columns
        WHERE table_name = UPPER(:table_name)
        ORDER BY column_id
        """
        return await self.execute_query(query, {"table_name": table_name})

    async def get_accessible_objects(self) -> List[Dict[str, Any]]:
        """Get list of accessible tables and views"""
        query = """
        SELECT owner, object_name, object_type 
        FROM all_objects 
        WHERE object_type IN ('TABLE', 'VIEW')
        AND owner NOT IN ('SYS', 'SYSTEM', 'AUDSYS', 'OUTLN', 'XDB')
        ORDER BY owner, object_type, object_name
        """
        return await self.execute_query(query)

    async def get_user_privileges(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get user roles and privileges"""
        roles = await self.execute_query("""
            SELECT granted_role, admin_option, default_role
            FROM user_role_privs
            ORDER BY granted_role
        """)
        
        privileges = await self.execute_query("""
            SELECT privilege 
            FROM session_privs
            ORDER BY privilege
        """)
        
        return {
            "roles": roles,
            "privileges": privileges
        }