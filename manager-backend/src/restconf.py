from fastapi import APIRouter, Request
from src.models import get_connection
from lxml import etree

router = APIRouter(prefix="/restconf")


def _elem_to_dict(el: etree._Element) -> dict | str:
    children = list(el)
    if not children:
        return el.text or ""
    result: dict = {}
    for child in children:
        tag = etree.QName(child).localname
        val = _elem_to_dict(child)
        if tag in result:
            existing = result[tag]
            result[tag] = [existing, val] if not isinstance(existing, list) else existing + [val]
        else:
            result[tag] = val
    return result


def _xml_to_dict(xml_bytes: bytes) -> dict:
    root = etree.fromstring(xml_bytes)
    data = root.find("{urn:ietf:params:xml:ns:netconf:base:1.0}data")
    if data is None:
        data = root
    return _elem_to_dict(data)


def _nc(filter_xml: str) -> dict:
    m = get_connection()
    reply = m.get_config(source="running", filter=("subtree", filter_xml))
    return _xml_to_dict(reply.xml.encode())


def _nc_get(filter_xml: str) -> dict:
    m = get_connection()
    reply = m.get(filter=("subtree", filter_xml))
    return _xml_to_dict(reply.xml.encode())


def _nc_edit(config_xml: str):
    m = get_connection()
    m.edit_config(target="running", config=config_xml)


@router.get("/data/ietf-interfaces:interfaces", operation_id="getInterfaces")
async def get_interfaces():
    filter_xml = '<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>'
    return _nc(filter_xml)


@router.get("/data/ietf-interfaces:interfaces/interface={name}", operation_id="getInterface")
async def get_interface(name: str):
    filter_xml = f"""
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface><name>{name}</name></interface>
    </interfaces>"""
    return _nc(filter_xml)


@router.put("/data/ietf-interfaces:interfaces/interface={name}", operation_id="putInterface")
async def put_interface(name: str, request: Request):
    body = await request.json()
    iface = body.get("ietf-interfaces:interface", body)
    iface["name"] = name
    config_xml = f"""
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{name}</name>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">{iface.get("type", "ianaift:ethernetCsmacd")}</type>
                <enabled>{str(iface.get("enabled", True)).lower()}</enabled>
            </interface>
        </interfaces>
    </config>"""
    _nc_edit(config_xml)
    return {"status": "ok"}


@router.delete("/data/ietf-interfaces:interfaces/interface={name}", operation_id="deleteInterface")
async def delete_interface(name: str):
    config_xml = f"""
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
                <name>{name}</name>
            </interface>
        </interfaces>
    </config>"""
    _nc_edit(config_xml)
    return {"status": "ok"}


@router.get("/data/ietf-system:system", operation_id="getSystem")
async def get_system():
    filter_xml = '<system xmlns="urn:ietf:params:xml:ns:yang:ietf-system"/>'
    return _nc(filter_xml)


@router.get("/data/ietf-yang-library:modules-state", operation_id="getModulesState")
async def get_modules_state():
    filter_xml = '<modules-state xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-library"/>'
    return _nc_get(filter_xml)
