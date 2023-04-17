import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class GPT:
    """
    messages=[
        {"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}
    ]

    <OpenAIObject chat.completion id=chatcmpl-768TJkfahS03985QOP1XSc8nUTxsO at 0x1c32fcd79c0> JSON:
    {
        "choices": [
            {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "Yes, as an AI language model, I have knowledge of Python programming language. However, my language abilities and programming knowledge are limited to what I have been taught and trained on.",
                "role": "assistant"
            }
            }
        ],
        "created": 1681696889,
        "id": "chatcmpl-768TJkfahS03985QOP1XSc8nUTxsO",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {
            "completion_tokens": 36,
            "prompt_tokens": 12,
            "total_tokens": 48
        }
    }
    """

    def __init__(self) -> None:
        self.gpt_model: str = "gpt-3.5-turbo"
        self.deep: int = 6
        self.messages: list[str] = []

    def turbo35(self, message: str):
        self.messages.append({"role": "user", "content": message})
        completion = openai.ChatCompletion.create(
            model=self.gpt_model, messages=self.messages
        )
        return completion.choices[0].message.content
