import sqlite3
import os
from datetime import datetime

# Initialize Database
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            deadline TEXT,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add a Task
def add_task(description, deadline):
    if not description.strip():
        print("Description cannot be empty.")
        return

    try:
        if deadline:
            datetime.strptime(deadline, "%Y-%m-%d")  # Validate date format
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, deadline, status) VALUES (?, ?, ?)",
                   (description, deadline, "pending"))
    conn.commit()
    conn.close()
    print("Task added successfully!")

# View All Tasks
def view_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("No tasks found.")
        return

    print("\nAll Tasks:")
    for task in tasks:
        print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2] or 'None'}, Status: {task[3]}")

# View Tasks by Status
def view_tasks_by_status(status):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print(f"No {status} tasks found.")
        return

    print(f"\n{status.capitalize()} Tasks:")
    for task in tasks:
        print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2] or 'None'}, Status: {task[3]}")

# Update a Task
def update_task(task_id, new_description=None, new_status=None):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if not task:
        print("Task ID not found.")
        conn.close()
        return

    if new_description:
        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
    if new_status:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))

    conn.commit()
    conn.close()
    print("Task updated successfully!")

# Delete a Task
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if not task:
        print("Task ID not found.")
        conn.close()
        return

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted successfully!")

# Main Menu
def main_menu():
    while True:
        print("\nTask Management System")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update a task")
        print("6. Delete a task")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD) or leave blank: ")
            add_task(description, deadline if deadline else None)

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            view_tasks_by_status("pending")

        elif choice == "4":
            view_tasks_by_status("completed")

        elif choice == "5":
            try:
                task_id = int(input("Enter task ID to update: "))
            except ValueError:
                print("Invalid task ID. Please enter a numeric value.")
                continue

            print("1. Update description")
            print("2. Mark as completed")
            sub_choice = input("Enter your choice: ")
            if sub_choice == "1":
                new_description = input("Enter new description: ")
                update_task(task_id, new_description=new_description)
            elif sub_choice == "2":
                update_task(task_id, new_status="completed")
            else:
                print("Invalid choice.")

        elif choice == "6":
            try:
                task_id = int(input("Enter task ID to delete: "))
            except ValueError:
                print("Invalid task ID. Please enter a numeric value.")
                continue
            delete_task(task_id)

        elif choice == "7":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Entry point for the program
if __name__ == "__main__":
    init_db()  # Ensure database is initialized
    main_menu()
