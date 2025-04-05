import sqlite3

DB_PATH = "database.db"

# ✅ Get Database Connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Ensure Tables Exist
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Create `bins` table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bins (
            bin_id TEXT PRIMARY KEY,
            location TEXT NOT NULL,
            weight INTEGER NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            status TEXT DEFAULT 'Not Collected'
        )
    """)

    # ✅ Create `collectors` table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS collectors (
            collector_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    """)

    # ✅ Create `bin_assignments` table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bin_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bin_id TEXT NOT NULL,
            user TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ✅ Save Bin Data (Fixed)
def save_bin_data(bin_id, weight, location, latitude, longitude):
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Check if bin exists
    cursor.execute("SELECT bin_id FROM bins WHERE bin_id = ?", (bin_id,))
    existing_bin = cursor.fetchone()

    if existing_bin:
        # ✅ Update existing bin
        cursor.execute("""
            UPDATE bins 
            SET weight = ?, location = ?, latitude = ?, longitude = ?
            WHERE bin_id = ?
        """, (weight, location, latitude, longitude, bin_id))
    else:
        # ✅ Insert new bin
        cursor.execute("""
            INSERT INTO bins (bin_id, weight, location, latitude, longitude, status)
            VALUES (?, ?, ?, ?, ?, 'Not Collected')
        """, (bin_id, weight, location, latitude, longitude))

    conn.commit()
    conn.close()

# ✅ Get All Collectors (Fixed)
def get_all_collectors():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT collector_id, name, phone, latitude, longitude FROM collectors")
    collectors = {}
    for row in cursor.fetchall():
        collectors[row["collector_id"]] = {
            "collector_id": row["collector_id"],
            "name": row["name"],
            "phone": row["phone"],
            "latitude": row["latitude"],
            "longitude": row["longitude"]
        }
    
    conn.close()
    return collectors

# ✅ Assign Bin to Collector (Fixed)
def assign_bin_to_collector(user, bin_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Ensure `bin_assignments` table exists
    cursor.execute("INSERT INTO bin_assignments (bin_id, user) VALUES (?, ?)", (bin_id, user))

    conn.commit()
    conn.close()
    print(f"✅ Bin {bin_id} assigned to {user} and saved to `bin_assignments`.")

# ✅ Get All Bins (Fixed)
def get_all_bins():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT bin_id, location, weight, latitude, longitude, status FROM bins")
    bins = []
    for row in cursor.fetchall():
        bins.append({
            "bin_id": row["bin_id"],
            "location": row["location"],
            "weight": row["weight"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "status": row["status"]
        })

    conn.close()
    return bins

# ✅ Initialize Database on First Run
initialize_database()
