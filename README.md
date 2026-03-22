# NETCONF-manager

source .venv/bin/activate
docker compose logs -f manager-backend

uv run netconf-console2 --host 172.18.0.1 --port 830 --get /modules-state