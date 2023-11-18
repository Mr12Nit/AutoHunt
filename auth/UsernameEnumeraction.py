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



class Enumerate:
	def __init__(self, TargetUrl,headers=None,postData=None,endpoint=None,data=None, invalidUsererrorMessage=None, usernamePart=None, passwordPart=None, usernameFile=None, passwordFile=None):
		self.TargetUrl = TargetUrl
		self.headers = headers
		self.data = data
		self.endpoint = endpoint
		self.invalidUsererrorMessage = invalidUsererrorMessage
		self.usernamePart = usernamePart
		self.passwordPart = passwordPart
		self.usernameFile = usernameFile
		self.passwordFile = passwordFile

	def ReadFile(self, fileName=None):
		try:
			if fileName:
				with open(fileName, 'r') as file:
					Lines = [line.strip() for line in file.readlines() if line.strip()]
					return Lines
		except:
			print(f"Error in reading file {fileName}")
      
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


	def enumerateUsername(self, username):
		if self.headers and self.endpoint and self.data and self.invalidUsererrorMessage :
			self.data[self.usernamePart] = username
			print("trying:",username,end='\r')
			response = self.sendPost()
			if self.checkResponseResult(response, self.invalidUsererrorMessage):
				return False
			else:
				return True
		else:
			print("all aruguments must be passed")
	
	def enumerateUsernameFromFile(self):
		if self.usernameFile:
			for i in self.ReadFile(self.usernameFile):
				userResult = self.enumerateUsername(i)
				if userResult:
					print(i," is a valid user")

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
			print("error in checking response")


	def sendRequest(self):
		try:
			login_data = {"username": self.username , "password": "temp"}
			session = requests.session()
			responce = session.post(self.TargetUrl, data=login_data)

			return [responce.text, responce.status_code]
		except:
			print("Error geting the request to ",self.TargetUrl)
 
	def checkIfInvalidErroExist(self, responseResult):
		if responseResult[1] == 200 :
			if self.invalidUsererrorMessage in responseResult[0]:
				return True
			else:
				return False
		else:
			print("response code is: ",responseResult[1]) # print the response code if the respons is not 200

	def checkIfValidUser(self, username):
		self.username = username
		result = self.sendRequest()
		return self.checkIfInvalidErroExist(result)
		


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Username Enumerateion script", add_help=False)
	parser.add_argument('--help', '-h', action='help', help='this is a help message')
	parser.add_argument('--url', type=str, help='Input Target Url')
	parser.add_argument('--headers', type=str, help='Input dictionary headers like {"key":"value"}')
	parser.add_argument('--postData', type=str, help='Input dictionary PostData like {"key":"value"}')
	parser.add_argument('--endpoint', type=str, help='Input str')
	parser.add_argument('--invalidUsererrorMessage', type=str, help='Input str')
	parser.add_argument('--usernameFile', type=str, help='Input str')
	parser.add_argument('--passwordFile', type=str, help='Input str')
	parser.add_argument('--usernamePart', type=str, help='Input str')
	parser.add_argument('--passwordPart', type=str, help='Input str')




	args = parser.parse_args()
	url = args.url
	headers = json.loads(args.headers) if args.headers else None
	PostData = json.loads(args.postData) if args.postData else None
	EndPoint = args.endpoint
	usernameFile = args.usernameFile
	passwordFile = args.passwordFile
	usernamePart = args.usernamePart
	passwordPart = args.passwordPart
	invalidUsererrorMessage = args.invalidUsererrorMessage


	Test = Enumerate(TargetUrl=url,headers=headers,data=PostData,endpoint=EndPoint,usernameFile=usernameFile,usernamePart=usernamePart, invalidUsererrorMessage=invalidUsererrorMessage)
	Test.enumerateUsernameFromFile()

