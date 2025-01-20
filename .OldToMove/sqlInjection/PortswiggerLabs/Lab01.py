# https://portswigger.net/web-security/all-labs

from sys import argv        # To pass argument into script 
import requests 


def SendPayload(TargetUrl, Payload):
	respond = requests.get(TargetUrl+Payload)
	print(respond.status_code)


def CheckSqlInjection(TargetUrl):
	Payload = ["'","''"]  # single qoute won't work douple will 
	BadRespond = requests.get(TargetUrl+Payload[1])
	GoodRespod = requests.get(TargetUrl+Payload[0])
	if BadRespond.status_code == 200 and GoodRespod.status_code != 200 : 
		print("Sql injection Detected ")


if __name__ == "__main__" :
	try:
		if len(argv) > 2:
			TargetUrl = argv[1]
			Payload = argv[2].strip()
			SendPayload(TargetUrl, Payload)
		else:
			TargetUrl = argv[1]
			CheckSqlInjection(TargetUrl)
	except:
		print("[url] [Payload] to send Payload\n[url] to only check for sql injection]")