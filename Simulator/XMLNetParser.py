import xml.etree.ElementTree as ET

def parse(xmlFile: str) -> (list, list, dict):
    root = ET.parse(xmlFile).getroot()
    nodes_xml = root[1][0]
    links_xml = root[1][1]
    nodes = []
    links = []
    capacities = {}
    for child in nodes_xml:
        node_id = child.attrib['id']
        nodes.append(node_id)
    for child in links_xml:
        source = child[0].text
        target = child[1].text
        links.append((source, target))
        links.append((target, source))
        modules = child[2]
        cap = 0
        for module in modules:
            cap += float(module[0].text)
        cap = cap/2
        capacities[(source, target)] = cap
        capacities[(target, source)] = cap
    return nodes, links, capacities

def parseTraffic(xmlFile: str) -> dict:
    root = ET.parse(xmlFile).getroot()
    demands_xml = root[2]
    demands = {}
    for demand in demands_xml:
        src = demand[0].text
        dst = demand[1].text
        trf = float(demand[2].text)
        demands[(src, dst)] = trf
    return demands