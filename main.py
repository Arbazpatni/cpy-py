import subprocess
import os
import time

# The cloud service usually gives you ONE port via an environment variable
public_port = os.environ.get("PORT", "3000") 

def run_server():
    binary_path = "./TCli"
    
    # Ensure it is executable
    os.chmod(binary_path, 0o755)

    print(f"Starting TCli server")
    
    # Start the process
    process = subprocess.Popen([binary_path, "start", "accept", "--token", "B8oXaAifqOPw+Sv6NexjzSqmuhw6a2DATWdjCh942R8=", public_port])

    while True:
        # Check if the process is still running
        if process.poll() is not None:
            print("TCli Server crashed! Restarting...")
            process = subprocess.Popen([binary_path, "start", "accept", "--token", "B8oXaAifqOPw+Sv6NexjzSqmuhw6a2DATWdjCh942R8=", public_port])
        
        time.sleep(10) # Check status every 10 seconds

if __name__ == "__main__":
    run_server()
