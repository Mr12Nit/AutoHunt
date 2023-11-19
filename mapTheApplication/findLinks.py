import requests
import re
from sys import path

path.append('/home/mr124/Project/BugHunting')
from BaseClass import BaseClass

if __name__ == '__main__':
	print("hello")
	url = 'https://en.wikipedia.org/wiki/TeX'
	response = BaseClass.BaseClass.sendGetRequest(url)
	links =  BaseClass.BaseClass.findLinks(response)
	if links:
		for i in links:
			print(i)