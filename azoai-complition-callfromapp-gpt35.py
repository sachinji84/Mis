import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Take environment variables from .env.
load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OAI_DEPLOYMENT_NAME")

client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview"
)

# This will correspond to the custom name you chose for your deployment when you deployed a model.
# Use a gpt-35-turbo-instruct deployment.
deployment_name = AZURE_OPENAI_DEPLOYMENT_NAME

# Send a completion call to generate an answer
prompt = "tell me about capital of india?"
response = client.completions.create(
    model=deployment_name,
    prompt=prompt,
    temperature=1,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)

print(prompt, "\nAnswer:" + response.choices[0].text)


# output 
# DELL@SachinKPC MINGW64 /d/Mytech/IDE_workspace/sachinji84git/AzureAI/Azureopenai-image-gen-api
# $ python azoai-complition-callfromapp-gpt35.py 
# tell me about capital of india? 
# Answer: hoe many states in india?Tel me some sities of Uttaranchalstate? which is largest desert in india? What is NATGRID & RTI? what is not natural but grow in many colours???? (Tie or clothes hanger ) What is the full form of SMS? Who invented electricity? Who discovered penicillin? Who is the CEO of IBM? Who is CTBT? Who wrote The Wealth Of Nations? Who was the Russian Communist Leader? Delhi became the Capital of India