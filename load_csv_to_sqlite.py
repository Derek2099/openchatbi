"""Load CSV files into SQLite database for OpenChatBI."""

import pandas as pd
import sqlite3
from pathlib import Path

# Configuration
DB_PATH = "data/sdtm/sdtm.db"
CSV_FILES = {
    "dm": "data/sdtm/dm.csv",
    "ae": "data/sdtm/ae.csv",
    "vs": "data/sdtm/vs.csv",
}

def load_csv_to_sqlite():
    """Load all CSV files into SQLite database."""
    # Create database directory if it doesn't exist
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing database to start fresh
    if db_path.exists():
        print(f"Removing existing database: {DB_PATH}")
        db_path.unlink()
    
    # Connect to SQLite database (creates if doesn't exist)
    print(f"Creating SQLite database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Load each CSV file into a table
        for table_name, csv_path in CSV_FILES.items():
            csv_file = Path(csv_path)
            
            if not csv_file.exists():
                print(f"Warning: CSV file not found: {csv_path}")
                continue
            
            print(f"Loading {csv_path} into table '{table_name}'...")
            
            # Read CSV with pandas
            df = pd.read_csv(csv_path)
            
            # Write to SQLite
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            # Verify
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  ✓ Loaded {count} rows into '{table_name}' table")
            
            # Show table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"  Columns: {', '.join([col[1] for col in columns])}")
        
        # Create indexes for better performance
        print("\nCreating indexes...")
        cursor = conn.cursor()
        
        # Index on USUBJID for all tables (common join key)
        for table_name in CSV_FILES.keys():
            try:
                cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_usubjid ON {table_name}(USUBJID)")
                print(f"  ✓ Created index on {table_name}.USUBJID")
            except Exception as e:
                print(f"  Warning: Could not create index on {table_name}.USUBJID: {e}")
        
        # Additional useful indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_dm_age ON dm(AGE)")
            print("  ✓ Created index on dm.AGE")
        except Exception as e:
            print(f"  Warning: Could not create index on dm.AGE: {e}")
        
        conn.commit()
        
        print("\n" + "="*60)
        print("✓ Database setup complete!")
        print(f"Database location: {db_path.absolute()}")
        print(f"Connection URI: sqlite:///{db_path.absolute()}")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error during database setup: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    load_csv_to_sqlite()
