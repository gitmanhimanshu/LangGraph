---
title: Image Generator SDXL
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.44.0"
python_version: "3.11"
app_file: app.py
pinned: false
---

# Simple Image Generator (SDXL)

Lightweight image generator using HuggingFace Inference API - no local model download needed!

## Advantages
- No GPU required
- No model download (uses cloud API)
- Fast setup
- Uses SDXL (best quality)

## Setup

1. Install:
```bash
pip install -r requirements.txt
```

2. Add your HF token to `.env`:
```
HUGGINGFACE_API_KEY=your_token_here
```

## Usage

### CLI:
```bash
python generate.py
```

### Web UI:
```bash
python app.py
```

## Note
Uses HuggingFace Inference API - requires internet connection and valid API token.
