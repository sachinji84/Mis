import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

# Take environment variables from .env.
load_dotenv()
# endpoint = os.getenv("ENDPOINT_URL", "https://sk-az-openai-1.openai.azure.com/")
# deployment = os.getenv("DEPLOYMENT_NAME", "skazoai1-gpt-35-turbo")
# token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OAI_DEPLOYMENT_NAME")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    # azure_ad_token_provider=token_provider,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview"
)

completion = client.chat.completions.create(
    # model=deployment,
    model=AZURE_OPENAI_DEPLOYMENT_NAME,
    messages=[
        {
            "role": "user",
            "content": "Can you tell me about capital of  Sikkim ?"
        }],
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

print(completion.choices[0].message.content)


# output
# DELL@SachinKPC MINGW64 /d/Mytech/IDE_workspace/sachinji84git/AzureAI/Azureopenai-image-gen-api
# $ python azoai-chat-callfromapp-gpt35.py 
# The capital of Sikkim is Gangtok. It is located in the eastern Himalayan range, at an altitude of 1,650 meters above sea level. Gangtok is a popular tourist destination, known for its scenic beauty and cultural significance. It is also the administrative and commercial center of Sikkim. The city has a mix of traditional and modern architecture, and is famous for its Buddhist monasteries, temples, and natural hot springs. Gangtok is well-connected by road and air, with regular flights and bus services from major cities in India.