import json
import subprocess
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to write"},
                    "content": {"type": "string", "description": "Content to write into the file"}
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command on the user's machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to execute"}
                },
                "required": ["command"],
            },
        },
    }
]

def execute_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    if name == "read_file":
        path = args.get("path")
        print(f"\n[Tool Call] Agentul vrea sa citeasca fisierul: {path}")
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
            
    elif name == "write_file":
        path = args.get("path")
        content = args.get("content")
        print(f"\n[ATENTIE] Agentul vrea sa SCRIE in fisierul: {path}")
        print(f"Continut:\n{content}\n")
        confirm = input("Aprobati scrierea? (y/n): ")
        if confirm.lower() != 'y':
            return "Error: User denied permission to write to this file."
        
        try:
            with open(path, "w") as f:
                f.write(content)
            return "File successfully written."
        except Exception as e:
            return f"Error writing file: {e}"
            
    elif name == "run_command":
        cmd = args.get("command")
        print(f"\n[ATENTIE] Agentul vrea sa EXSECUTE comanda: {cmd}")
        confirm = input("Aprobati executia? (y/n): ")
        if confirm.lower() != 'y':
            return "Error: User denied permission to run this command."
            
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return f"Command executed successfully.\nOutput:\n{result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"Command failed with exit code {e.returncode}.\nError Output:\n{e.stderr}"
        except Exception as e:
            return f"Error executing command: {e}"

    return "Unknown tool"

def main():
    print("Coding Agent pornit. Puteti cere scrierea sau rularea unui cod.")
    messages = [
        {"role": "system", "content": "You are a coding assistant. You can read files, write files, and run terminal commands to help the user solve programming tasks. Always verify if your scripts work by running them."}
    ]
    
    while True:
        try:
            user_input = input("\nTu: ")
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
                    result = execute_tool(tool_call)
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
