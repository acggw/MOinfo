import pandas as pd 
from notifications import notificaton
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

HOUSE_BILLS_LINK = "https://documents.house.mo.gov/xml/251-BillList.XML"

def get_bills(datetime: str, current_time: str) -> [notificaton]:
    Notifications = []
    #Notifications.extend(get_house_bills(datetime))
    Notifications.extend(get_senate_bills(datetime))
    return Notifications

def get_house_bills(last_ran: str, current_time: str) -> [notificaton]:
    UPDATED = 5
    BILL_LINK = 4
    ACTION = 1

    Notifications = []

    bills = get_xml_data(HOUSE_BILLS_LINK)
    for bill in bills:
        #if(bill[UPDATED].text.split(" ")[0])
        data = requests.get(bill[BILL_LINK].text)
        if(str(data) != "<Response [200]>"):
            #log
            print("Error fetching data from " + bill[BILL_LINK].text)
            print(str(data))
            continue
        #log
        print("Data fetched from " + bill[BILL_LINK].text)

        info = ET.fromstring(data.text)[0]
        last_action = info.find("LastAction").text.split(" - ")    
        titles = info.find("Title")
        title = titles.find("ShortTitle").text
        description = titles.find("LongTitle").text

        bill_string = info.find("CurrentBillString").text

        msg = "Update on Bill " + bill_string + " " + title + " - " + description + " - " + last_action[ACTION]
        Notifications.append(notificaton(msg))
    
    return Notifications


def get_senate_bills(datetime: str, current_time: str) -> [notificaton]:
    LINK = "https://www.senate.mo.gov/25Info/BTS_Web/Daily.aspx?SessionType=R&ActionDate="

    data = requests.get(LINK + datetime).text
    soup = BeautifulSoup(data, "html.parser")
    bill_elements = soup.find_all("dl")

    bills = []
    for dl in bill_elements:
        text = " ".join(dl.get_text(separator=" ", strip=True).split())
        bills.append(notificaton(text))

    return bills


def get_xml_data(link: str):
    data = requests.get(link)

    if(str(data) != "<Response [200]>"):
        #log
        print("Error fetching data from " + ALL_BILLS_LINK)
        print(str(data))
        return
    
    #log
    print("Data fetched from " + link)
    root = ET.fromstring(data.text)
    #print(type(root))
    return root
