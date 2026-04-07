# Text to Image Generator

Stable Diffusion based text-to-image generator with Gradio UI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your Hugging Face token to `.env`:
```
HUGGINGFACE_API_KEY=your_token_here
```

## Usage

### Simple Generation
```bash
python generate.py
```

### Gradio UI
```bash
python app.py
```

## Models

- Default: `runwayml/stable-diffusion-v1-5`
- Upgrade to SDXL for better quality (requires more VRAM)

## Tips

- Use descriptive prompts with style keywords
- Examples: "ultra realistic, 4k, cinematic lighting"
- GPU recommended (5-10 sec vs 1-5 min on CPU)
