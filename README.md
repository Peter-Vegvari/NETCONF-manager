# NETCONF-manager

uv sync --all-extras --dev
source .venv/bin/activate

sudo docker run -d --rm --name notconf-test -v $(pwd)/test/yang-modules:/yang-modules ghcr.io/notconf/notconf:21987110689-debug

uv run netconf-console2 --host $(sudo docker inspect notconf-test --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}') --port 830 --get /modules-state
