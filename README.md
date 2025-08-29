# MLflow Public Read-Only

This repository provides a minimal MLflow server setup with artifacts hosted on a public S3/Swift bucket on Chameleon Cloud. Users can explore existing using this setup

## Architecture

Host mounts the public S3 bucket via `rclone`. MLflow container reads mounted folder as artifact root: