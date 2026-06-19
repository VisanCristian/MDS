import json
import requests
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate an arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The expression to evaluate, e.g. '2 + 3 * 4'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a specific latitude and longitude.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location"
                    }
                },
                "required": ["latitude", "longitude"],
            },
        },
    }
]

def execute_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    if name == "calculate":
        print(f"[Tool Call] calculate({args['expression']})")
        try:
            # using eval with basic math operators for safety could be better, but eval is requested by example
            return str(eval(args["expression"], {"__builtins__": None}, {}))
        except Exception as e:
            return f"Error evaluating expression: {e}"
            
    elif name == "get_weather":
        print(f"[Tool Call] get_weather(lat={args['latitude']}, lon={args['longitude']})")
        try:
            response = requests.get("https://api.open-meteo.com/v1/forecast", params={
                "latitude": args["latitude"],
                "longitude": args["longitude"],
                "current_weather": True
            })
            data = response.json().get("current_weather", {})
            return f"{data.get('temperature')}°C, wind {data.get('windspeed')} km/h"
        except Exception as e:
            return f"Error fetching weather: {e}"
            
    return "Unknown tool"

def main():
    print("Agent pornit (scrie 'exit' sau 'quit' pentru a iesi).")
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the provided tools when needed. If the user asks for weather and doesn't specify coordinates, ask for them or use a default (Bucharest is 44.43, 26.10)."}
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
