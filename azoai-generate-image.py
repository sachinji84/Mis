# Note: DALL-E 3 requires version 1.0.0 of the openai-python library or later
import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv

# Take environment variables from .env.
load_dotenv()
# Code of your application, which uses environment variables (e.g. from `os.environ` or `os.getenv`)
# as if they came from the actual environment.
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OAI_ENDPOINT")


# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_version="2024-05-01-preview",
    # azure_endpoint="https://sk-genai-practice1.openai.azure.com/",
    # api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY
)

# Call the model
result = client.images.generate(
    model="Dalle3",  # the name of your DALL-E 3 deployment
    prompt="provide me an image of fish doing catwalk",
    n=1
)

image_url = json.loads(result.model_dump_json())['data'][0]['url']
print(image_url)

# result
# DELL@SachinKPC MINGW64 /d/Mytech/IDE_workspace/sachinji84git/AzureAI/Azureopenai-image-gen-api
# $ python azoai-generate-image.py
# https://dalleproduse.blob.core.windows.net/private/images/06e43ef8-666c-43dc-9e36-7ca27cb51c85/generated_00.png?se=2024-08-17T09%3A57%3A42Z&sig=hYzumGYMXY3vn7IPRbS%2BSzwajfG2XCZi0ggzv34LRAg%3D&ske=2024-08-22T12%3A26%3A54Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-08-15T12%3A26%3A54Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02