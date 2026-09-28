import json

from brave_search import scrape_content, search_brave
from openai import OpenAI


class ChatModel:
    def __init__(self, model: str, system_prompt: str = None, api_key: str = '', name: str = None):
        self.model = model
        self.client = OpenAI(api_key = api_key)
        self.chat_history: list[dict[str, str]] = []
        self.name = name
        
        if system_prompt:
            self.add_message("system", system_prompt)

    def add_message(self, role: str, content: str) -> None:
        self.chat_history.append({
            "role": role,
            "content": content,
            "name": self.name
        })

    def clear_history(self) -> None:
        self.chat_history = []

    def get_history(self) -> list[dict[str, str]]:
        return self.chat_history

    def generate(self, message: str, **kwargs) -> str:
        self.add_message("user", message)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
            **kwargs
        )
        
        assistant_message = response.choices[0].message.content
        
        self.add_message("assistant", assistant_message)
        
        return response
    

class SearchModel(ChatModel):
    def tool_call(self, tool_call) -> dict:
        tool_id = tool_call.id
        arguments = json.loads(tool_call.function.arguments)

        if tool_call.function.name == 'search_brave':
            print("Searching for information...\n")
            query = arguments['query']
            result = search_brave(query)

        elif tool_call.function.name == 'scrape_content':
            print("Scraping content...\n")
            url = arguments['url']
            result = scrape_content(url)
            
        tool_response = {'role':'tool', 'content': result, 'tool_call_id': tool_id}

        return tool_response
    

    def format_tool_response(self, tool_call):
        formatted_dict = {
        "role": "assistant",
        "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "arguments": tool_call.function.arguments,
                        "name": tool_call.function.name
                    }
                }
            ]
        }

        return formatted_dict
    

    def generate(self, message: str, **kwargs) -> str:
        self.add_message("user", message)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
            **kwargs
        )

        if not response.choices[0].message.content:
            

            tool_completion = response.choices[0].message.tool_calls[0]
            tool_response = self.tool_call(tool_completion)

            messages = self.chat_history + [self.format_tool_response(tool_completion)] + [tool_response]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )

        assistant_message = response.choices[0].message.content
        self.add_message("assistant", assistant_message)
    
        return response