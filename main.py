import os
import shutil
import subprocess
import platform
import stat
import time

def get_binary():
    """Detects CPU architecture and returns the matching filename."""
    arch = platform.machine().lower()
    
    if "arm" in arch or "aarch64" in arch:
        print(f"Detected ARM architecture: {arch}")
        return "TCli_arm"
    elif "x86" in arch or "amd64" in arch:
        print(f"Detected x86_64 architecture: {arch}")
        return "TCli"  # Your original x86_64 file
    else:
        raise RuntimeError(f"Unsupported architecture: {arch}")

def deploy_and_run():
    source_name = get_binary()
    target_path = os.path.join("/tmp", source_name)
    
    # 1. Check if the source file actually exists in your upload
    if not os.path.exists(source_name):
        print(f"Error: Source file {source_name} not found in the app directory!")
        return

    # 2. Copy to /tmp to bypass Read-Only Filesystem
    try:
        shutil.copy2(source_name, target_path)
        # Grant Read/Write/Execute permissions
        os.chmod(target_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
        print(f"Binary deployed to {target_path}")
    except Exception as e:
        print(f"Failed to copy binary: {e}")
        return

    # 3. Continuous Execution Loop
    cmd = [target_path, "start", "accept", "--token", "B8oXaAifqOPw+Sv6NexjzSqmuhw6a2DATWdjCh942R8="]
    
    while True:
        print(f"Launching {source_name}...")
        try:
            # We use .wait() to keep the Python script alive while the C app runs
            process = subprocess.Popen(cmd)
            process.wait() 
            print("Process exited. Restarting in 10 seconds...")
        except Exception as e:
            print(f"Execution error: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    deploy_and_run()
