import json
import sys
import os
from datetime import datetime
from openai import OpenAI

# Adaugam directorul parinte (MDS) in sys.path pentru a importa aplicatia
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Task
from storage import load_tasks, save_tasks, get_next_id

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the task scheduler.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the task"},
                    "description": {"type": "string", "description": "Short description of the task"},
                    "deadline": {"type": "string", "description": "Deadline in format DD-MM-YYYY HH:MM"},
                    "start_time": {"type": "string", "description": "Start time in format DD-MM-YYYY HH:MM"},
                    "end_time": {"type": "string", "description": "End time in format DD-MM-YYYY HH:MM"},
                    "priority": {"type": "string", "description": "Priority: low, medium, or high"}
                },
                "required": ["title", "deadline", "start_time", "end_time", "priority"],
            },
        },
    }
]

def add_task_tool(args):
    tasks = load_tasks()
    new_task = Task(
        id=get_next_id(tasks),
        title=args.get("title", "Untitled"),
        description=args.get("description", ""),
        deadline=args.get("deadline", ""),
        start_time=args.get("start_time", ""),
        end_time=args.get("end_time", ""),
        priority=args.get("priority", "medium").lower(),
    )
    tasks.append(new_task)
    save_tasks(tasks)
    return f"Task '{new_task.title}' added with ID {new_task.id}."

def main():
    print("Agent Task Scheduler pornit. Poti adauga un task scriind in limbaj natural.")
    current_year = datetime.now().year
    current_date = datetime.now().strftime("%d-%m-%Y")
    
    messages = [
        {"role": "system", "content": f"You are a task scheduler assistant. The current year is {current_year} and today is {current_date}. When the user asks to add a task, use the add_task tool. If time is not specified, assume default sensible values (e.g. 09:00 for start time and 17:00 for deadline/end time). Extract dates exactly into the required format DD-MM-YYYY HH:MM. Ensure all required fields are passed."}
    ]
    
    while True:
        try:
            user_input = input("\nComanda (ex: 'Adauga un task pentru taxe pana pe 25 mai'): ")
            if user_input.lower() in ['exit', 'quit']:
                break
        except (EOFError, KeyboardInterrupt):
            break
            
        messages.append({"role": "user", "content": user_input})
        
        while True:
            response = client.chat.completions.create(
                model="mistral",
                messages=messages,
                tools=tools,
            )
            msg = response.choices[0].message
            messages.append(msg)
            
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    if tool_call.function.name == "add_task":
                        args = json.loads(tool_call.function.arguments)
                        print(f"\n[Executare Tool] add_task: {args}")
                        try:
                            result = add_task_tool(args)
                        except Exception as e:
                            result = f"Error adding task: {e}"
                            
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        })
            else:
                print(f"\nAgent: {msg.content}")
                break

if __name__ == "__main__":
    main()
