import os
import getpass
from urllib.parse import urlparse

RCLONE_CONF_DIR = os.path.expanduser("~/.config/rclone")
RCLONE_CONF_PATH = os.path.join(RCLONE_CONF_DIR, "rclone.conf")

def get_container_name(link_or_name: str) -> str:
    """
    Extract container name from URL or return the plain name.
    """
    if link_or_name.startswith("http"):
        path = urlparse(link_or_name).path
        return path.rstrip("/").split("/")[-1]
    return link_or_name

def write_rclone_swift_config(ec2_id, ec2_secret, endpoint):
    os.makedirs(RCLONE_CONF_DIR, exist_ok=True)
    config_content = f"""
[rclone_s3]
provider = Ceph
access_key_id = {ec2_id}
secret_access_key = {ec2_secret}
endpoint = {endpoint}
"""
    
    with open(RCLONE_CONF_PATH, "w") as f:
        f.write(config_content)
    print(f"Rclone Swift config written to {RCLONE_CONF_PATH}")

def main():
    print("=== setup rclone for public object store container ===")
    
    container1 = input("Enter metrices container name or full URL: ").strip()
    container2 = input("Enter artifacts container name or full URL: ").strip()
    
    container1_name = get_container_name(container1)
    container2_name = get_container_name(container2)
    
    ec2_id = input("🦎 Enter Swift application_credential_id: ").strip()
    ec2_secret = getpass.getpass("🦎 Enter Swift application_credential_secret (it will not be visible when typing): ").strip()
    endpoint = input("🦎 Enter Swift auth URL (e.g., https://chi.uc.chameleoncloud.org:5000/v3): ").strip()
    
    write_rclone_swift_config(ec2_id, ec2_secret, endpoint)
    
    # Generate mount shell script in $HOME
    mount_script = f"""#!/bin/bash
mkdir -p /mnt/public-metrics /mnt/public-artifacts
sudo chown -R cc /mnt/public-artifacts
sudo chown -R cc /mnt/public-metrics

rclone mount rclone_s3:{container1_name} /mnt/public-metrics \\
    --allow-other \\ 
    --daemon \\
    --vfs-cache-mode writes \\
    

rclone mount rclone_s3:{container2_name} /mnt/public-artifacts \\
    --allow-other \\ 
    --daemon \\
    --vfs-cache-mode writes \\
    
echo "containers mounted at /mnt/public-metrics and /mnt/public-artifacts"
"""
    script_path = os.path.expanduser("/mnt/mount_public_swift.sh")
    with open(script_path, "w") as f:
        f.write(mount_script)
    os.chmod(script_path, 0o755)
    print(f"✅ Mount script written to {script_path}")
    print(f"Run it using: bash {script_path}")

if __name__ == "__main__":
    main()