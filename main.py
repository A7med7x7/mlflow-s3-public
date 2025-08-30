import os
import getpass
from urllib.parse import urlparse

RCLONE_CONF_DIR = os.path.expanduser("~/.config/rclone")
RCLONE_CONF_PATH = os.path.join(RCLONE_CONF_DIR, "rclone.conf")

def get_container_name(link_or_name: str) -> str:
    """Extract container name from URL or return as-is if plain name."""
    if link_or_name.startswith("http"):
        path = urlparse(link_or_name).path
        return path.rstrip("/").split("/")[-1]
    return link_or_name

def write_rclone_swift_config(user_id, app_id, app_secret, auth_url, region):
    os.makedirs(RCLONE_CONF_DIR, exist_ok=True)
    config_content = f"""
[rclone_swift]
type = swift
user_id = {user_id}
application_credential_id = {app_id}
application_credential_secret = {app_secret}
auth = {auth_url}
region = {region}
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
    
    user_id = input("Enter Swift user_id: ").strip()
    app_id = input("Enter Swift application_credential_id: ").strip()
    app_secret = getpass.getpass("Enter Swift application_credential_secret: ").strip()
    auth_url = input("Enter Swift auth URL (e.g., https://chi.uc.chameleoncloud.org:5000/v3): ").strip()
    region = input("Enter Swift region (e.g., CHI@UC): ").strip()
    
    write_rclone_swift_config(user_id, app_id, app_secret, auth_url, region)
    
    # Generate mount shell script in $HOME
    mount_script = f"""#!/bin/bash
mkdir -p /mnt/public-metrics /mnt/public-artifacts

rclone mount rclone_swift:{container1_name} /mnt/public-metrics \\
    --config /home/cc/.config/rclone/rclone.conf \\
    --vfs-cache-mode full \\
    --daemon \\
    --allow-non-empty \\
    --allow-other

rclone mount rclone_swift:{container2_name} /mnt/public-artifacts \\
    --config /home/cc/.config/rclone/rclone.conf \\
    --vfs-cache-mode full \\
    --daemon \\
    --allow-non-empty \\
    --allow-other
    
echo "containers mounted at /mnt/public-metrics and /mnt/public-artifacts"
"""
    script_path = os.path.expanduser("/mnt/mount_public_swift.sh")
    with open(script_path, "w") as f:
        f.write(mount_script)
    os.chmod(script_path, 0o755)
    print(f"Mount script written to {script_path}")
    print(f"Run it using: bash {script_path}")

if __name__ == "__main__":
    main()