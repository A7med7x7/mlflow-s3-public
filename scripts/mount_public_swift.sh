sudo chown -R cc /mnt/public-metrics
sudo chgrp -R cc /mnt/public-artifacts
sudo chown -R cc /mnt/public-metrics
sudo chgrp -R cc /mnt/public-artifacts



rclone mount rclone_swift:UC-NODE-mlflow-metrics /mnt/public-metrics \
    --vfs-cache-mode full \
    --daemon \
    --read-only \
    --allow-non-empty \
    --allow-root

rclone mount rclone_swift:UC-NODE-mlflow-artifacts /mnt/public-artifacts \
    --vfs-cache-mode full \
    --daemon \
    --read-only \
    --allow-non-empty \
    --allow-root
    
echo "containers mounted at ~/public-metrics and ~/public-artifacts"