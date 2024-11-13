## Text Generation using OpenAI-LLM
## One go code
# from google.colab import userdata
from openai import OpenAI
from dotenv import load_dotenv
import os

# Take environment variables from .env.
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=OPENAI_API_KEY)
print(type(client))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "you are a funny assistant who describe everything in funniest way"},
        {"role": "user", "content": "compose a poem for the indian people"}
    ]
)
print(response.choices[0].message.content)