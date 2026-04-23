# Task 14: Fetch Todos from API and Print Titles of First 5 Items
import requests

# Fetch data from API
response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = response.json()  # Convert JSON response to Python list

# Print titles of first 5 todos
for todo in todos[:5]:
    print(todo['title'])