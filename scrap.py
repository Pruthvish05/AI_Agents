import json
import openai

# 1. Define a custom tool (e.g., getting system time or fetching data)
def get_current_weather(location: str):
    """Get the current weather for a given location."""
    return json.dumps({"location": location, "temperature": "22°C", "condition": "Sunny"})

# Map the function name to the actual Python callable
available_tools = {
    "get_current_weather": get_current_weather
}

tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "city": "The city and state, e.g. Bengaluru, India"}
                },
                "required": ["location"]
            }
        }
    }
]

# 2. Run the Agent Loop
def run_agent(user_prompt):
    messages = [{"role": "user", "content": user_prompt}]
    
    # Send user request and tool definitions to the LLM
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools_definition
    )
    
    response_message = response.choices[0].message
    
    # Check if the LLM decided it needs to call a tool
    if response_message.tool_calls:
        messages.append(response_message) # Append assistant's intent to call tool
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_tools[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            # Execute the local Python function
            tool_output = function_to_call(**function_args)
            
            # Send the tool output back to the LLM so it can formulate the final answer
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": tool_output,
            })
            
        second_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return second_response.choices[0].message.content
        
    return response_message.content

print(run_agent("What's the weather like in Bengaluru right now?"))