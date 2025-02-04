import asyncio
from server import execute_query

async def test_connection():
    try:
        # Test basic connection with a simple query
        results = await execute_query("SELECT SYSDATE FROM DUAL")
        print("Connection successful!")
        print("Current database time:", results[0])
        
        # Test accessible tables and views
        print("\nChecking accessible objects...")
        results = await execute_query("""
            SELECT owner, object_name, object_type 
            FROM all_objects 
            WHERE object_type IN ('TABLE', 'VIEW')
            AND owner NOT IN ('SYS', 'SYSTEM', 'AUDSYS', 'OUTLN', 'XDB')
            ORDER BY owner, object_type, object_name
        """)
        
        if results:
            print("\nAccessible objects by schema:")
            current_owner = None
            current_type = None
            
            for row in results:
                owner = row['OWNER']
                obj_type = row['OBJECT_TYPE']
                
                if owner != current_owner:
                    print(f"\nSchema: {owner}")
                    current_owner = owner
                    current_type = None
                
                if obj_type != current_type:
                    print(f"\n  {obj_type}s:")
                    current_type = obj_type
                
                print(f"    - {row['OBJECT_NAME']}")
        else:
            print("\nNo accessible tables or views found.")
            print("\nChecking your database privileges...")
            
            # Check user's roles
            print("\nChecking roles...")
            roles = await execute_query("""
                SELECT granted_role, admin_option, default_role
                FROM user_role_privs
                ORDER BY granted_role
            """)
            
            if roles:
                print("\nYour roles:")
                for role in roles:
                    print(f"- {role['GRANTED_ROLE']} (Default: {role['DEFAULT_ROLE']})")
            else:
                print("No roles found.")
            
            # Check direct privileges
            print("\nChecking system privileges...")
            privs = await execute_query("""
                SELECT privilege 
                FROM session_privs
                ORDER BY privilege
            """)
            
            if privs:
                print("\nYour system privileges:")
                for priv in privs:
                    print(f"- {priv['PRIVILEGE']}")
            else:
                print("No direct system privileges found.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
        # If we hit an error, let's try a simpler query to list tables
        try:
            print("\nTrying alternative approach to list tables...")
            results = await execute_query("""
                SELECT username, account_status
                FROM all_users
                WHERE username NOT IN ('SYS', 'SYSTEM', 'AUDSYS', 'OUTLN', 'XDB')
                ORDER BY username
            """)
            
            print("\nAvailable database users:")
            for row in results:
                print(f"- {row['USERNAME']} (Status: {row['ACCOUNT_STATUS']})")
                
        except Exception as e2:
            print(f"Additional error: {str(e2)}")

if __name__ == "__main__":
    asyncio.run(test_connection())