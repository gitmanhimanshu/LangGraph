import os
from huggingface_hub import InferenceClient
import gradio as gr

# Initialize client - HF Spaces automatically provides token
client = InferenceClient(token=os.getenv("HF_TOKEN"))

def generate(prompt, width=1024, height=1024):
    """Generate image using SDXL"""
    try:
        image = client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0",
            width=width,
            height=height
        )
        return image
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(
            label="Prompt",
            placeholder="A dragon flying over mountains, cinematic lighting...",
            lines=3
        ),
        gr.Slider(512, 1024, value=1024, step=128, label="Width"),
        gr.Slider(512, 1024, value=1024, step=128, label="Height")
    ],
    outputs=gr.Image(label="Generated Image"),
    title="SDXL Image Generator",
    description="Generate high-quality images using Stable Diffusion XL",
    examples=[
        ["A dragon flying over mountains, cinematic lighting, 4k", 1024, 1024],
        ["Anime style cat, studio ghibli, detailed", 1024, 1024],
        ["Futuristic city at sunset, cyberpunk, neon lights", 1024, 1024]
    ]
)

if __name__ == "__main__":
    demo.launch()
