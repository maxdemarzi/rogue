import sys
import duckdb
from pyrel_duckdb import Model, Float, Integer, String, Date, DateTime, Boolean

def validate():
    # Try importing ontology
    print("Importing ontology...")
    try:
        import ontology
        model = ontology.model
        con = ontology.con
    except ImportError as e:
        print(f"Error importing ontology: {e}")
        print("Please ensure ontology.py exists and is syntactically correct.")
        sys.exit(1)
        
    print("Fetching active DuckDB tables and schemas...")
    tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
    schema_info = {}
    for t in tables:
        columns = con.execute(f"PRAGMA table_info({t})").fetchall()
        schema_info[t] = {col[1]: col[2] for col in columns}
        
    errors = 0
    warnings = 0
    
    print("\n=== STARTING SCHEMA DRIFT VALIDATION ===")
    for name, concept in sorted(model._concepts.items()):
        table = concept.table_name
        print(f"\nConcept: {name} (table: '{table}')")
        
        if table not in schema_info:
            # Check if this concept is a pure logical dimension (no table in DB)
            # Ticker, Date, CIK etc might not have physical tables if they are only referenced.
            # But let's check if the table should exist or if it's purely dimensional.
            logical_dimensions = ['ticker', 'cik', 'domain', 'industry', 'sector', 'rating', 'date', 'publisher', 'fundingstage']
            if table.lower() in logical_dimensions:
                print(f"  -> Pure logical dimension (no table '{table}' in DB)")
                continue
            print(f"  [ERROR] Table '{table}' does not exist in DuckDB catalog!")
            errors += 1
            continue
            
        # Check primary key column existence
        pk_columns = list(concept.identify_by.keys())
        for pk in pk_columns:
            if pk not in schema_info[table]:
                print(f"  [ERROR] Primary Key column '{pk}' does not exist in table '{table}'!")
                errors += 1
            else:
                print(f"  - PK: '{pk}' ({schema_info[table][pk]})")
                
        # Check each property
        for prop_name, prop in sorted(concept.properties.items()):
            # Skip if it is a primary key property already printed
            if prop_name in pk_columns:
                continue
                
            column = prop.column_name
            if not column:
                continue
                
            if column not in schema_info[table]:
                print(f"  [ERROR] Property '{prop_name}' mapped to missing column '{column}' in table '{table}'!")
                errors += 1
                continue
                
            col_type = schema_info[table][column].upper()
            
            # Check type compatibility
            expected_primitive = prop.target_type
            is_concept = prop.is_concept_to_concept
            
            if is_concept:
                # Concept-to-concept relationship
                print(f"  - Ref Property: '{prop_name}' -> col: '{column}' ({col_type})")
            else:
                # Primitive property
                prim_name = getattr(expected_primitive, '__name__', str(expected_primitive))
                print(f"  - Primitive Property: '{prop_name}' -> col: '{column}' ({col_type}) | Expected: {prim_name}")
                
                # Basic validation warnings/errors
                if expected_primitive == Float and 'DOUBLE' not in col_type and 'FLOAT' not in col_type and 'REAL' not in col_type and 'DECIMAL' not in col_type and 'NUMERIC' not in col_type:
                    print(f"    [WARNING] Type mismatch: Property expected Float, column is {col_type}")
                    warnings += 1
                elif expected_primitive == Integer and 'INT' not in col_type and 'BIGINT' not in col_type:
                    print(f"    [WARNING] Type mismatch: Property expected Integer, column is {col_type}")
                    warnings += 1
                elif expected_primitive == String and 'VARCHAR' not in col_type and 'TEXT' not in col_type and 'CHAR' not in col_type:
                    print(f"    [WARNING] Type mismatch: Property expected String, column is {col_type}")
                    warnings += 1
                elif expected_primitive == Date and 'DATE' not in col_type and 'TIMESTAMP' not in col_type:
                    print(f"    [WARNING] Type mismatch: Property expected Date, column is {col_type}")
                    warnings += 1
                    
    print("\n=== VALIDATION SUMMARY ===")
    print(f"Errors found: {errors}")
    print(f"Warnings found: {warnings}")
    
    con.close()
    if errors > 0:
        sys.exit(1)
    else:
        print("Schema validation PASSED!")

if __name__ == '__main__':
    validate()
