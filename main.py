from wikipedia_scraper_env import WikipediaScraper

def main():
    #create a WikipediaScraper
    Scraper = WikipediaScraper()

    #create a JSON-file with the first paragraph of each leader added
    Scraper.to_json_file()

#if __name__ == "__main__":
#    main()