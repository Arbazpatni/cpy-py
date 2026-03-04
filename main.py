import sys
import os
import shutil
import subprocess
import platform
import stat
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- 1. Tiny Web Server to satisfy Back4app Health Checks ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server(port):
    server = HTTPServer(('0.0.0.0', int(port)), HealthCheckHandler)
    print(f"Health check server started on port {port}")
    server.serve_forever()


def deploy_and_run():
    # 1. Architecture Detection
    arch = platform.machine().lower()
    if "arm" in arch or "aarch64" in arch:
        source_name = "TCli_arm"
    elif "x86" in arch or "amd64" in arch:
        source_name = "TCli"
    else:
        print(f"Unsupported architecture: {arch}")
        sys.exit(1)

    # 2. Setup Writable Working Directory
    # We use /tmp to ensure it works even on read-only filesystems
    base_tmp = "/tmp/tmon"
    target_binary = os.path.join(base_tmp, source_name)
    
    if not os.path.exists(base_tmp):
        os.makedirs(base_tmp, exist_ok=True)

    # 3. Copy & Permissions
    try:
        if os.path.exists(source_name):
            shutil.copy2(source_name, target_binary)
            # Mark as executable: rwx------
            os.chmod(target_binary, stat.S_IRWXU)
            print(f"--- Environment Ready ---")
            print(f"Arch: {arch} | Binary: {target_binary}")
        else:
            print(f"Error: {source_name} not found in current directory.")
            sys.exit(1)
    except Exception as e:
        print(f"Setup Error: {e}")
        sys.exit(1)

    # 3.1. Start Health Check in a background thread
    # This tells Back4app: "Yes, I am listening on the port you want!"
    assigned_port = os.environ.get("PORT", "3001")
    threading.Thread(target=run_health_server, args=(assigned_port,), daemon=True).start()

    # 4. Execution Configuration
    # It's better to get the token from an Environment Variable for Docker
    token = os.environ.get("TOKEN", "B8oXaAifqOPw+Sv6NexjzSqmuhw6a2DATWdjCh942R8=")
    cmd = [target_binary, "start", "accept", "--token", token]

    # 5. Continuous Restart Loop
    while True:
        print(f"\n[{time.ctime()}] Launching {source_name}...")
        try:
            # Set HOME and CWD to /tmp so the C program can write its config/logs
            env_vars = dict(os.environ, HOME=base_tmp, XDG_CONFIG_HOME=base_tmp)
            
            process = subprocess.Popen(
                cmd, 
                cwd=base_tmp, 
                env=env_vars,
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True
            )

            # Stream the output to the Docker logs
            for line in process.stdout:
                print(f"[TCli]: {line.strip()}")
            
            process.wait()
            print(f"Process exited with code {process.returncode}. Restarting...")
        except Exception as e:
            print(f"Runtime Error: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    deploy_and_run()
