import requests
from urllib.parse import urlparse
from urllib3 import disable_warnings,exceptions
disable_warnings(exceptions.InsecureRequestWarning)
import json
import argparse
from os import system


from sys import path as sysPath
from os import path as osPath

current_script_dir = osPath.dirname(osPath.abspath(__file__))
project_folder = osPath.abspath(osPath.join(current_script_dir, '..'))
sysPath.append(project_folder)

from BaseClass import BaseClass


proxy_url = 'http://127.0.0.1:8080'
proxies = {
    'http': proxy_url,
    'https': proxy_url,
}

class PostTraversal:
    def __init__(self, TargetUrl, headers=None, data=None, endpoint=None, PostTraversal=None,GetTraversal=None):
        self.TargetUrl = TargetUrl
        self.hostName = self.getHostname(TargetUrl)
        self.headers = headers
        self.data = data
        self.endpoint = endpoint
        self.payloads = ""
        self.PostTraversal = PostTraversal
        self.GetTraversal = GetTraversal


    def getHostname(self,url):
        parsedUrl = urlparse(url)
        return parsedUrl.hostname

    def checkResultTraversal(self, response):
        if response.status_code == 200 and "root" in response.text :
            return True
        else:
            return False

    def checkPathTraversalGet(self):
        # not ready yet iam just bored to make it i will use the tool
        if self.GetTraversal:
            for i in self.payloads:
                self.TargetUrl = self.TargetUrl.replace(self.GetTraversal,i)
                response = requests.get(self.TargetUrl)
                if self.checkResultTraversal(response):
                    print(f"found Path Traversal {i} \t\t {self.TargetUrl}")
                    return True
    
    def checkPathTraversalPost(self):
        pass


    def runDotdotpwn(self):
        if self.GetTraversal and BaseClass.BaseClass.chekcTool("dotdotpwn"):
            self.TargetUrl = self.TargetUrl.replace(self.GetTraversal,"TRAVERSAL")
            command = f'dotdotpwn -m http-url -u {self.TargetUrl} -k "root" -b '
            print(f"running Path Traversal on {self.TargetUrl}")
            system(f'echo -e "\\n" | {command}')






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path Traversal", add_help=False)
    parser.add_argument('--help', '-h', action='help', help='this is a help message')
    parser.add_argument('--url', type=str, help='Input Url')
    parser.add_argument('--headers', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--postData', type=str, help='Input dictionary PostData like {"key":"value"}')
    parser.add_argument('--endpoint', type=str, help='Input str')
    parser.add_argument('--TestTraversal', type=str, help='Input which will be the payload')


    args = parser.parse_args()
    url = args.url
    headers = json.loads(args.headers) if args.headers else None
    PostData = json.loads(args.postData) if args.postData else None
    EndPoint = args.endpoint
    TestTraversal = args.TestTraversal

    Test = PostTraversal(TargetUrl=url,headers=headers,data=PostData,endpoint=EndPoint,GetTraversal=TestTraversal)
    Test.runDotdotpwn()

    