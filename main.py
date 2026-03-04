import os
import shutil
import subprocess
import platform
import stat
import time

def deploy_and_run():
    # 1. Architecture Detection
    arch = platform.machine().lower()
    source_name = "TCli_arm" if ("arm" in arch or "aarch64" in arch) else "TCli"
    
    # 2. Setup Writable Paths
    base_tmp = "/tmp/tmon"
    target_binary = os.path.join(base_tmp, source_name)
    
    if not os.path.exists(base_tmp):
        os.makedirs(base_tmp)

    # 3. Copy & Permissions
    try:
        shutil.copy2(source_name, target_binary)
        os.chmod(target_binary, 0o777) 
        print(f"Ready: {target_binary} on {arch}")
    except Exception as e:
        print(f"Setup Error: {e}")
        return

    # 4. The Command
    cmd = [target_binary, "start", "accept", "--token", "B8oXaAifqOPw+Sv6NexjzSqmuhw6a2DATWdjCh942R8="]

    while True:
        print(f"Starting {source_name} at {time.ctime()}...")
        try:
            # We set 'cwd' so it writes logs/configs to /tmp
            # We set 'HOME' so it doesn't try to use /root or /home/user
            env_vars = dict(os.environ, HOME=base_tmp, XDG_CONFIG_HOME=base_tmp)
            
            process = subprocess.Popen(cmd, cwd=base_tmp, env=env_vars)
            process.wait()
            print("Process stopped. Restarting...")
        except Exception as e:
            print(f"Runtime Error: {e}")
        
        time.sleep(15)

if __name__ == "__main__":
    deploy_and_run()
