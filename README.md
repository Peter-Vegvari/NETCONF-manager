# NETCONF-manager

source .venv/bin/activate
docker compose logs -f manager-backend

uv run netconf-console2 --host 172.18.0.1 --port 830 --get /modules-state

sudo docker container prune
sudo docker compose up --force-recreate --build

npx openapi-typescript ./path/to/api/v1.yaml -o ./src/lib/api/v1.d.ts