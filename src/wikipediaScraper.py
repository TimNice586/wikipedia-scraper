# type: ignore
import requests
from bs4 import BeautifulSoup
import json

class WikipediaScraper():
    def __init__(self):
        """initializing the class with attributes:
        base_url: containing the base url of the API (https://country-leaders.onrender.com)
        country_endpoint: endpoint to get the list of supported countries
        leaders_endpoint: endpoint to get the list of leaders for a specific country
        cookies_endpoint: endpoint to get a valid cookie to query the API
        leaders_data: a (empty) dictionary for storing the data we will capture and finally output
        session: a session for speeding up requests to the API
        cookie: a dictionary being the cookie used for the API calls
        countries: a list containg the countries supported from the API (after calling get_countries)"""
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookies_endpoint = "/cookie"
        self.leaders_data = {}
        self.session = requests.session()
        self.cookie = {}
        self.countries = []

    def refresh_cookie(self) -> dict:
        """returns a new cookie if the cookie has expired"""
        cookie_url = f"{self.base_url}{self.cookies_endpoint}"
        self.cookie = self.session.get(cookie_url).cookies.get_dict()
        return self.cookie

    def get_countries(self) -> list:
        """returns a list of the supported countries from the API"""
        countries_url = f"{self.base_url}{self.country_endpoint}"
        self.countries = self.session.get(countries_url, cookies=self.refresh_cookie()).json()
        return self.countries

    def get_first_paragraph(self, wikipedia_url: str) -> str:
        """returns the first paragraph with details about the leader"""
        #define a user-agent to impersonate a browser to be able to scrape wikipedia sites (2 many requests from bots get blocked)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"}
        soup = BeautifulSoup(self.session.get(wikipedia_url,headers = headers).text, "html.parser")
        for paragraph in soup.find_all("p"):
        #check if paragraph starts with bold text, is not empty and his second name is found in the paragraph
            if paragraph.find("b") == paragraph.contents[0] and paragraph.contents[0] != None and (soup.find("title").get_text().split()[1] in paragraph.get_text() or soup.find("title").get_text() in paragraph.get_text()):
                first_paragraph = paragraph.get_text().strip()
                return first_paragraph

    def get_leader(self) -> None:
        """"populates the leader_data object with the leaders of a country retrieved from the API and adds the first paragraph of their wiki-url"""
        #get the countries
        leaders_url = f"{self.base_url}{self.leaders_endpoint}"
        countries = self.get_countries()
        #loop over them and save their leaders in a dictionary
        #-> dict of {countries : list of dict for each leader}
        self.leaders_data= { country : self.session.get(leaders_url,cookies=self.refresh_cookie(),params={"country": country}).json() for country in countries}
        for country, leaders in self.leaders_data.items():
                for leader in leaders:
                    leader_url = leader["wikipedia_url"]
                    leader["first_paragraph"]=self.get_first_paragraph(leader_url)
        return self.leaders_data

    def to_json_file(self) -> None:
        """stores the data structure into a JSON file"""
        with open("leaders.json","w",encoding="utf-8") as file:
        #"dumps/writes" our leaders into a file named leaders.json, the indent and ascii are to make it more readable and pretty print it
            json.dump(self.get_leader(), file, indent=4, ensure_ascii=False)

WS = WikipediaScraper()
WS.to_json_file()