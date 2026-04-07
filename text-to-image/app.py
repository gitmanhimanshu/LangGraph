import gradio as gr
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

def generate(prompt):
    """Generate image from text prompt"""
    image = pipe(prompt).images[0]
    return image

# Create Gradio interface
demo = gr.Interface(
    fn=generate,
    inputs=gr.Textbox(
        label="Enter your prompt",
        placeholder="A dragon flying over mountains, cinematic lighting...",
        lines=3
    ),
    outputs=gr.Image(label="Generated Image"),
    title="Text to Image Generator",
    description="Generate images from text using Stable Diffusion",
    examples=[
        ["A dragon flying over mountains, cinematic lighting, ultra realistic, 4k"],
        ["Anime style cat, studio ghibli, detailed"],
        ["Futuristic city at sunset, cyberpunk style, neon lights"]
    ]
)

if __name__ == "__main__":
    demo.launch()
