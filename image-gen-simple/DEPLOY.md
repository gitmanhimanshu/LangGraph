# Hugging Face Spaces Deployment Guide

## Steps to Deploy:

1. **Create Space**
   - Go to: https://huggingface.co/spaces
   - Click "Create new Space"
   - Name: `image-generator-sdxl`
   - SDK: Select **Gradio**
   - Hardware: **CPU Basic** (free)

2. **Upload Files**
   Upload these files to your Space:
   - `app.py`
   - `requirements.txt`
   - `README.md`

3. **Set Token (Important!)**
   - Go to Space Settings
   - Add Secret:
     - Name: `HF_TOKEN`
     - Value: Your Hugging Face token

4. **Done!**
   - Space will automatically build and deploy
   - Takes 2-3 minutes
   - Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/image-generator-sdxl`

## Why This Works:
- Uses Inference API (no GPU needed locally)
- Lightweight (no model download)
- Free tier compatible
- Auto-scales

## Note:
- `.env` file NOT needed on Spaces (uses Secrets instead)
- Token automatically available as `HF_TOKEN` environment variable
