import os
import sys
import time
import zipfile
import shutil
import subprocess
import requests
from config import UPDATE_ZIP_URL

def update_application():
    print("Starting update process...")
    print("Waiting for application to close...")
    time.sleep(2)  # Give main app time to close
    
    # 2. Download update
    print(f"Downloading update from {UPDATE_ZIP_URL}...")
    try:
        response = requests.get(UPDATE_ZIP_URL, stream=True)
        response.raise_for_status()
        
        zip_path = "update.zip"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
        
        # 3. Extract update
        print("Extracting update...")
        extract_folder = "update_extracted"
        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)
        os.makedirs(extract_folder)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
            
        # 4. Move files
        # GitHub zips usually have a root folder like "repo-main"
        # We need to find that folder and move its contents
        content_dir = extract_folder
        items = os.listdir(extract_folder)
        if len(items) == 1 and os.path.isdir(os.path.join(extract_folder, items[0])):
            content_dir = os.path.join(extract_folder, items[0])
            
        print(f"Installing files from {content_dir}...")
        
        # Copy files to current directory
        current_script = os.path.basename(__file__)
        
        for item in os.listdir(content_dir):
            s = os.path.join(content_dir, item)
            d = os.path.join(os.getcwd(), item)
            
            # Skip overwriting the running updater script to avoid errors
            if item == current_script:
                print(f"Skipping self-update for {item}...")
                continue
                
            try:
                if os.path.isdir(s):
                    # For directories, we need to be careful
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
                print(f"Updated: {item}")
            except Exception as e:
                print(f"Failed to update {item}: {e}")
                
        print("Update installed successfully.")
        
        # 5. Cleanup
        try:
            os.remove(zip_path)
            shutil.rmtree(extract_folder)
        except Exception as e:
            print(f"Cleanup warning: {e}")
        
        # 6. Restart application
        print("Restarting application...")
        if sys.platform == 'win32':
            subprocess.Popen([sys.executable, 'main.py'])
        else:
            subprocess.Popen([sys.executable, 'main.py'])
            
        sys.exit(0)
        
    except Exception as e:
        print(f"\nFATAL ERROR during update: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    update_application()
