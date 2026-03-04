import os
import shutil
import subprocess
import stat

# 1. Define paths
source_binary = "TCli"           # Where the file is in your upload
target_binary = "/tmp/TCli"      # The only writable spot

# 2. Copy the binary to /tmp
try:
    shutil.copy2(source_binary, target_binary)
    print(f"Successfully moved binary to {target_binary}")
except Exception as e:
    print(f"Error moving file: {e}")

# 3. Grant execution permissions (Crucial!)
os.chmod(target_binary, stat.S_IRWXU) # Gives Read, Write, and Execute to the user

# 4. Run it from the new location
try:
    process = subprocess.Popen([target_binary, "start", "accept", "--token", "B8oXaAifqOPw+Sv6NexjzSqmuhw6a2DATWdjCh942R8=", "3000"])
    print("Server is running from /tmp")
except Exception as e:
    print(f"Execution failed: {e}")
