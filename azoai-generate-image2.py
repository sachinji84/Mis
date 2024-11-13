import requests
import time
import os
from dotenv import load_dotenv


def main():

    try:
        # Get Azure OpenAI Service settings
        load_dotenv()
        api_base = os.getenv("AZURE_OAI_ENDPOINT")
        api_key = os.getenv("AZURE_OAI_KEY")
        api_version = '2024-02-15-preview'  # 2024-05-01-preview

        # Get prompt for image to be generated
        prompt = input("\nEnter a prompt to request an image: ")

        # Call the DALL-E model
        url = "{}openai/deployments/dalle3/images/generations?api-version={}".format(api_base, api_version)
        # for url you will see Delle3 model is got deployed in Azure OpenAI Studio and target URI wil be
        # https://sk-genai-practice1.openai.azure.com/openai/deployments/Dalle3/images/generations?api-version=2024-02-01
        headers = {"api-key": api_key, "Content-Type": "application/json"}
        body = {
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        response = requests.post(url, headers=headers, json=body)

        # Get the revised prompt and image URL from the response
        revised_prompt = response.json()['data'][0]['revised_prompt']
        image_url = response.json()['data'][0]['url']

        # Display the URL for the generated image
        print(revised_prompt)
        print(image_url)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()


# result
#
# DELL@SachinKPC MINGW64 /d/Mytech/IDE_workspace/sachinji84git/AzureAI/Azureopenai-image-gen-api
# $ python azoai-generate-image2.py
# Enter a prompt to request an image: giraffe flying a kite
#
# A tall giraffe with a patterned coat of brown patches separated by white lines. 
# The giraffe is standing in a vast, sunny savannah with sparse acacia trees in the background. 
# Tied to the Giraffe's long, winding tail is a vibrant kite soaring high in the bright, clear sky. 
# The kite is in a classic diamond shape, filled with bold stripes of red, blue and green colors. 
# The giraffe appears to be amused, craning its long neck to watch the colorful kite swoosh and gyrate amidst the playful gusts of wind.
#
# https://dalleproduse.blob.core.windows.net/private/images/ca789251-c94a-42fb-8adc-1fc80b8a80b0/generated_00.png?se=2024-08-17T09%3A59%3A40Z&sig=Zu4VfmuUeZV2FmQI3uLKFpWPp9i2TF89R3JxF6GXRS4%3D&ske=2024-08-23T09%3A25%3A21Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-08-16T09%3A25%3A21Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02