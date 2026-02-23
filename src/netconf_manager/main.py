from fastapi import FastAPI
from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager
from ncclient import manager

# uv run fastapi dev src/netconf_manager/main.py
app = FastAPI()
host = "172.18.0.1"
port = 830
username = "admin"
password = "admin"


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    with manager.connect(
        host="172.18.0.1",
        port=830,
        username="admin",
        password="admin",
        hostkey_verify=False,
        device_params={'name': 'iosxr'}
    ) as m:
        schema = m.get_schema('ietf-netconf-monitoring')
        print(schema.data)


if __name__ == "__main__":
    main()
