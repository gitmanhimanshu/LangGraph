from diffusers import StableDiffusionPipeline
import torch
from huggingface_hub import login
import os
from dotenv import load_dotenv

load_dotenv()

# Login to Hugging Face
login(os.getenv("HUGGINGFACE_API_KEY"))

# Load the model
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)

# Use GPU if available, else CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)

# Memory optimization
pipe.enable_attention_slicing()

def generate_image(prompt, output_path="output.png"):
    """Generate image from text prompt"""
    print(f"Generating image on {device}...")
    image = pipe(prompt).images[0]
    image.save(output_path)
    print(f"Image saved to {output_path}")
    return image

if __name__ == "__main__":
    prompt = "A dragon flying over mountains, cinematic lighting, ultra realistic, 4k"
    generate_image(prompt)
