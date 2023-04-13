from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import openai
import re

app = FastAPI()

openai.api_key = "xxxx"


class Prompt(BaseModel):
    prompt: str


class Response(BaseModel):
    text: str


# https://github.com/satory074/discordbot_chatgpt_sample/blob/main/main.py が参考になるかも。
@app.post("/completions")
async def completions(message: List[Prompt]):
    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=texts[0].prompt,
    #     temperature=0.7,
    #     max_tokens=1000,
    #     n=1,
    #     stop=None,
    # )

    escape_content: str = re.sub(
        r"<@(everyone|here|[!&]?[0-9]{17,20})> ", "", message[0].prompt)

        # openaiに送るメッセージ
    messages: list[dict[str, str]] = [{"role": "user", "content": escape_content}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)

    reply: str = "\n".join([choice["message"]["content"] for choice in response["choices"]])

    return reply


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000,
                reload=True, workers=1, log_level="info")
