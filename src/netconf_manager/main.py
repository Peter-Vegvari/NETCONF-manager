from fastapi import FastAPI
from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager

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
    with connect_ssh(host, port, username, password) as session:
        mgr = Manager(session, timeout=5)
        print(mgr.get().data_xml)


if __name__ == "__main__":
    main()
