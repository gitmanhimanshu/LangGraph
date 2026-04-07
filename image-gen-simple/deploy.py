import os
from huggingface_hub import HfApi, create_repo
from dotenv import load_dotenv

load_dotenv()

# Configuration
USERNAME = "himanshuyada70"
SPACE_NAME = "image-generator-sdxl"
TOKEN = os.getenv("HUGGINGFACE_API_KEY")

def deploy_to_spaces():
    """Deploy app to Hugging Face Spaces"""
    
    # Initialize API
    api = HfApi(token=TOKEN)
    
    # Create repo ID
    repo_id = f"{USERNAME}/{SPACE_NAME}"
    
    print(f"Creating Space: {repo_id}")
    
    try:
        # Create Space
        create_repo(
            repo_id=repo_id,
            token=TOKEN,
            repo_type="space",
            space_sdk="gradio",
            private=False
        )
        print(f"✅ Space created: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print(f"Space already exists or error: {e}")
    
    # Upload files
    files_to_upload = [
        "app.py",
        "requirements.txt",
        "README.md"
    ]
    
    print("\nUploading files...")
    for file in files_to_upload:
        try:
            api.upload_file(
                path_or_fileobj=file,
                path_in_repo=file,
                repo_id=repo_id,
                repo_type="space",
                token=TOKEN
            )
            print(f"✅ Uploaded: {file}")
        except Exception as e:
            print(f"❌ Error uploading {file}: {e}")
    
    print(f"\n🚀 Deployment complete!")
    print(f"🔗 Your app: https://huggingface.co/spaces/{repo_id}")
    print(f"\n⚠️ IMPORTANT: Add HF_TOKEN secret in Space Settings!")
    print(f"   Go to: https://huggingface.co/spaces/{repo_id}/settings")
    print(f"   Add Secret: HF_TOKEN = {TOKEN[:10]}...")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Error: HUGGINGFACE_API_KEY not found in .env file")
    else:
        deploy_to_spaces()
