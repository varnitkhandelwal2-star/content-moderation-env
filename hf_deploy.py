import os
import sys
from huggingface_hub import HfApi

def deploy():
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("Error: HF_TOKEN environment variable is not set.")
        print("Please obtain a token from https://huggingface.co/settings/tokens (with WRITE permission).")
        sys.exit(1)
        
    api = HfApi(token=token)
    try:
        username = api.whoami()["name"]
    except Exception as e:
        print(f"Error authenticating with token: {e}")
        sys.exit(1)
        
    repo_id = f"{username}/content-moderation-env"
    
    print(f"Creating Hugging Face Space: {repo_id}...")
    try:
        api.create_repo(repo_id=repo_id, repo_type="space", space_sdk="docker", exist_ok=True)
    except Exception as e:
        print(f"Error creating repo: {e}")
        sys.exit(1)
        
    print("Uploading files to the Space...")
    files_to_upload = [
        "env.py", "inference.py", "tasks.py", "openenv.yaml", 
        "Dockerfile", "requirements.txt", "README.md"
    ]
    
    for file in files_to_upload:
        if os.path.exists(file):
            print(f"Uploading {file}...")
            try:
                api.upload_file(
                    path_or_fileobj=file,
                    path_in_repo=file,
                    repo_id=repo_id,
                    repo_type="space"
                )
            except Exception as e:
                print(f"Failed to upload {file}: {e}")
        else:
            print(f"Warning: {file} not found locally.")

    print("\n" + "="*50)
    print(f"Deployment complete!")
    print(f"Your space is now building at: https://huggingface.co/spaces/{repo_id}")
    print("="*50)

if __name__ == "__main__":
    deploy()
