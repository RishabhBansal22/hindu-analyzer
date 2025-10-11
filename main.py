from scripts.gemini import Gemini
from scripts.scrapper import Scrapper
import json


def main(num_articles:int=1):
    gemini = Gemini()
    scraper = Scrapper(url="https://www.thehindu.com/opinion/editorial/")

    try:
        output = scraper.scrape_articles(num_articles=num_articles)
        print("succesfully scrapped articles")
        if output:
            print("parsing output to python dict")
            output_dict = json.loads(output)
            
            summary_list = []
            for article in output_dict["articles"]:
                res = gemini.gemini_response(user_prompt=article["content"])
                summary_list.append(res)
            
            return summary_list
    except Exception as e:
        print(e)


output = main()
for i in output:
    print(i)
