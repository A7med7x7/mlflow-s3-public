#!/bin/bash
sudo mkdir -p /mnt/public-metrics
sudo chown -R cc /mnt/
sudo chgrp -R cc /mnt/


rclone mount rclone_swift: /mnt/public-metrics \
    --vfs-cache-mode full \
    --read-only \
    --allow-non-empty