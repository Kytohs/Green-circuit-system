from database import save_collector_data

# Add waste collectors
save_collector_data("collector1", "John Doe", "+254758293126", -1.2833, 36.8219)  # Nairobi
save_collector_data("collector2", "Jane Smith", "+254758293126", -1.2921, 36.8219)  # Another location

print("Collectors added successfully!")
