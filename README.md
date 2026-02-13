# NETCONF-manager

uv sync --all-extras --dev
source .venv/bin/activatecs
uv run netconf-console2 --host $(sudo docker inspect notconf-test --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}') --port 830 --get /modules-state