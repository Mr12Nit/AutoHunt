import requests
from sys import argv



class Request:
	def __init__(self, TargetUrl, invalidUsererrorMessage) -> None:
		self.TargetUrl = TargetUrl
		self.invalidUsererrorMessage = invalidUsererrorMessage
		self.username = "testuser"

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
		



if __name__ == '__main__' :
	with open(argv[3]) as f:
		AllUsers = f.read().splitlines()

	validUsers = []
	r = Request( argv[1] ,argv[2])
	for user in AllUsers:
		userResult = r.checkIfValidUser(user)
		if not userResult:
			validUsers.append(user)
	for i in validUsers:
		print(i)
