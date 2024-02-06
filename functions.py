import requests
from lxml import etree as ET
# from xml.etree import ElementTree as ET

# U may override it
mw = "https://www.mathworks.com/help/ref/data"
namespace = {"mw": mw}

# Fetch the XML file
# Download the XML file
def download_xml(url, filename):

    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)

def parse_xml(filename):
    # Parse the downloaded XML file
    global root
    global tree
    tree = ET.parse(filename)
    root = tree.getroot()
    return tree, root


def get_all_title(elem):
    str_out = ""
    while True:
        if elem.getparent() is None:
            break
        elem = elem.getparent()
        # print(">", elem.tag, elem.attrib)
        if elem.find("mw:title", namespace) is not None:
            # print("GOTIT", elem.find("mw:title", namespace).text)
            if str_out:
                str_out = f'{elem.find("mw:title", namespace).text} > {str_out}'
            else:
                str_out = f'{elem.find("mw:title", namespace).text}'

        # print(elem.find("mw.title", namespace))
    return str_out

def get_purpose(elem):
    return elem.find("mw:purpose", namespace).text


def get_url(elem):
    return elem.attrib["target"]