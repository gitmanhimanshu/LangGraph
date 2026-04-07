import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# Initialize client
client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))

def generate_image(prompt, output_path="output.png"):
    """Generate image using SDXL via Inference API"""
    print(f"Generating image for: {prompt}")
    
    image = client.text_to_image(
        prompt,
        model="stabilityai/stable-diffusion-xl-base-1.0",
        width=1024,
        height=1024
    )
    
    image.save(output_path)
    print(f"Image saved to {output_path}")
    return image

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    generate_image(prompt)
