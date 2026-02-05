import os
import json
from openai import OpenAI
from sqlmodel import Session, select
from models import engine, Message, Todo, Task 
from mcp_tools import add_task, get_tasks, mark_task_complete, delete_task

# 1. Groq Client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# 2. Complete Tools List
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new todo task",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Details"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "List all tasks",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_task_complete",
            "description": "Mark a specific task as complete using its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task from the list using its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task"}
                },
                "required": ["task_id"]
            }
        }
    }
]

def run_agent(user_prompt: str, conversation_id: int):
    messages = [
        {"role": "system", "content": "You are a Smart Task Manager. Use tools to Add, View, Delete, or Complete tasks. To delete or complete, you might need to 'get_tasks' first to find the ID."},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            f_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if f_name == "add_task":
                add_task(args.get("title"), args.get("description", ""))
                return f"✅ Done! Added: {args.get('title')}"

            elif f_name == "get_tasks":
                tasks = get_tasks()
                if not tasks: return "No tasks found."
                return "Your Tasks:\n" + "\n".join([f"ID: {t.id} - {t.title} [{'Done' if t.completed else 'Pending'}]" for t in tasks])

            elif f_name == "mark_task_complete":
                mark_task_complete(args.get("task_id"))
                return f"✔️ Task {args.get('task_id')} marked as complete!"

            elif f_name == "delete_task":
                delete_task(args.get("task_id"))
                return f"🗑️ Task {args.get('task_id')} has been deleted."

    return response_message.content