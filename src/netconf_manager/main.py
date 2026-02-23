from fastapi import FastAPI
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

    with manager.connect(host=host, port=830,
                         username=username, hostkey_verify=False, device_params={'name':'iosxr'}) as m:
        c = m.get_config(source='running').data_xml
        with open("%s.xml" % host, 'w') as f:
            f.write(c)


if __name__ == "__main__":
    main()
