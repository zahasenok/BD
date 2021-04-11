import xml.etree.ElementTree as ET

def displayLinks():
    mytree = ET.parse('outputs/xsport.xml')
    myroot = mytree.getroot()
    print("HyperLinks : \n")
    for page in myroot:
        print(page.attrib['url'])

displayLinks()

