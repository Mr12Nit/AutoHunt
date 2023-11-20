import requests
import re
from sys import path as sysPath
from os import path as osPath

current_script_dir = osPath.dirname(osPath.abspath(__file__))
project_folder = osPath.abspath(osPath.join(current_script_dir, '..'))
sysPath.append(project_folder)

from BaseClass import BaseClass

if __name__ == '__main__':
	print("hello")
	url = 'https://en.wikipedia.org/wiki/TeX'
	response = BaseClass.BaseClass.sendGetRequest(url)
	links =  BaseClass.BaseClass.findLinks(response)
	if links:
		for i in links:
			print(i)