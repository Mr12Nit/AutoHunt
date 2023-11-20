import requests
import re
from bs4 import BeautifulSoup
from sys import path as sysPath
from os import path as osPath
import json
import argparse


current_script_dir = osPath.dirname(osPath.abspath(__file__))
project_folder = osPath.abspath(osPath.join(current_script_dir, '..'))
sysPath.append(project_folder)

from BaseClass import BaseClass

logger = BaseClass.log("mapApp", LogFile='mapApp.log')

class MapApp:
    def __init__(self, url) -> None:
        self.logger = logger
        self.url = url

    def findHttpLinks(self, response):
        try:
            if response.status_code == 200:
                url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                links = re.findall(url_pattern, response.text)
                self.logger.info(f"done finding the urls in the link {response.url}")
                return links
            else:
                self.logger.error("response code is not 200")
        except:
            self.logger.error("error in finding links")
    
    def findHrefLinks(self, response):
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                all_href_attributes = [tag.get('href') for tag in soup.find_all(attrs={'href': True})]
                all_href_attributes = list(set(all_href_attributes))
                newLinks = []
                for i in all_href_attributes:
                    if i.startswith("//"):
                        newLinks.append("https://"+i[1:])
                    elif i.startswith("http"):
                        newLinks.append(i)
                    elif i.startswith("/"):
                        newLinks.append(response.url[:-1]+i)
                    else:
                        newLinks.append(response.url[:-1]+i)
                self.logger.info(f"done finding all href links in the url {response.url}")
                return newLinks
            else:
                self.logger.error("response code is not 200")
        except Exception as e:
            self.logger.error("Can't find href links")


    def findAllLinks(self, response):
        href = self.findHrefLinks(response)
        http = self.findHttpLinks(response)
        if href and http:
            http.extend(href)
            return list(set(http))
    
    


if __name__ == '__main__':
    print("hellp")
    parser = argparse.ArgumentParser(description="Map the application and find entry points ", add_help=False)
    parser.add_argument('--help', '-h', action='help', help='this is a help message')
    parser.add_argument('--url', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--headers', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--postData', type=str, help='Input dictionary PostData like {"key":"value"}')
    parser.add_argument('--endPoint', type=str, help='Input str')



    args = parser.parse_args()
    url = args.url
    headers = json.loads(args.headers) if args.headers else None
    postData = json.loads(args.postData) if args.postData else None
    endPoint = args.endPoint

    x = MapApp(url=url)
    response = BaseClass.BaseClass.sendGetRequest(url)
    links = x.findAllLinks(response)
    BaseClass.BaseClass.writeToFile("links.txt",links)
