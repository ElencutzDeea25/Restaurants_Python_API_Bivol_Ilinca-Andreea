import json

# Sample data
data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

# Specify the file path
file_path = "rest.json"

# Write data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f'Data has been written to {file_path}')