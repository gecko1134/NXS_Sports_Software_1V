
#!/usr/bin/env bash
set -e
docker build -t nxs-master-os .
docker run --rm -it -p 8501:8501 --env-file deploy/.env.example nxs-master-os
