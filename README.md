# NETCONF-manager

uv sync --all-extras --dev
source .venv/bin/activate

sudo docker run -d --rm --name notconf-test -v $(pwd)/test/yang-modules:/yang-modules ghcr.io/notconf/notconf:21987110689-debug

uv run netconf-console2 --host 172.18.0.1 --port 830 --get /modules-state