# type: ignore
import requests
from bs4 import BeautifulSoup
import json

def get_first_paragraph(wikipedia_url, session):
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"}
   soup = BeautifulSoup(session.get(wikipedia_url,headers = headers).text, "html.parser")
   for paragraph in soup.find_all("p"):
      #check if paragraph starts with bold text, is not empty and his second name is found in the paragraph
      if paragraph.find("b") == paragraph.contents[0] and paragraph.contents[0] != None and (soup.find("title").get_text().split()[1] in paragraph.get_text() or soup.find("title").get_text() in paragraph.get_text()):
         first_paragraph = paragraph.get_text()
         return first_paragraph
      

def get_leaders():
    #define the urls
    countries_url = "https://country-leaders.onrender.com/countries"
    leaders_url = "https://country-leaders.onrender.com/leaders"
    cookie_url = "https://country-leaders.onrender.com/cookie" 
    #get the cookies (store them in a session object)
    session = requests.session()
    cookies = session.get(cookie_url).cookies.get_dict() #dict of cookies {name cookie: value cookie}
    #get the countries
    countries = session.get(countries_url, cookies=cookies).json()
    #loop over them and save their leaders in a dictionary
    #-> dict of {countries : list of dict for each leader}
    leaders_per_country= { country : session.get(leaders_url,cookies=cookies,params={"country": country}).json() for country in countries}
    for country, leaders in leaders_per_country.items():
            for leader in leaders:
                leader_url = leader["wikipedia_url"]
                leader["first_paragraph"]=get_first_paragraph(leader_url, session)
    return leaders_per_country

def save(leaders_per_country):
    #save leaders_per_country to JSON file
    with open("leaders.json","w",encoding="utf-8") as file:
        json.dump(leaders_per_country, file, indent=4, ensure_ascii=False)


save(get_leaders())