import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all bins
cursor.execute("SELECT * FROM bins")
bins = cursor.fetchall()

print("✅ Bins Table:")
for bin in bins:
    print(bin)

# Fetch all collectors
cursor.execute("SELECT * FROM collectors")
collectors = cursor.fetchall()

print("\n✅ Collectors Table:")
for collector in collectors:
    print(collector)

# Close connection
conn.close()
