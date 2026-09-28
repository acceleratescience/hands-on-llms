import os
import base64
from openai import OpenAI

def ocr(image_path, prompt='', client=None):
    if client is None:
        client = OpenAI(
            base_url="https://llm.science.ai.cam.ac.uk",
            api_key=os.getenv("SPLINTER_API_KEY")
        )
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    base64_image = encode_image(image_path)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    response = client.chat.completions.create(
        model="Qwen/Qwen3.6-27B-FP8",
        messages=messages,
        temperature=1.0,
        top_p=0.95,
        presence_penalty=1.5,
        extra_body={
            "top_k": 20,
            "chat_template_kwargs": {"enable_thinking": False},
        }, 
    )

    return response.choices[0].message.content
