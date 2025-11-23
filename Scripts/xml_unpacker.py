from notification_class import notification
import requests 
import xml.etree.ElementTree as ET

def get_xml_data(link: str):
    data = requests.get(link)

    if(str(data) != "<Response [200]>"):
        #log
        print("Error fetching data from " + link)
        print(str(data))
        return
    
    #log
    print("Data fetched from " + link)
    root = ET.fromstring(data.text)
    #print(type(root))
    return root