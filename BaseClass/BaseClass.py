import logging
import os
import subprocess
import requests
import re

def log(LoggerName, LogFile=None):
        # .debug .info .warning .error .critical
        # Create a logger for your script
        logger = logging.getLogger(LoggerName)
        logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        if LogFile:
                # Create a file handler for writing log messages to a file
                file_handler = logging.FileHandler(LogFile)
                file_handler.setLevel(logging.DEBUG)  # Set the desired log level
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)  

        # Create a stream handler for displaying log messages on the console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)  # Set the desired log level
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
        return logger

logger = log("BaseClass","log.txt")


class BaseClass:

    @staticmethod
    def ReadFile(Path):
        if BaseClass.checkIfFileExist(Path):
            try:
                with open(Path, 'r') as file:
                    Lines = [line.strip() for line in file.readlines() if line.strip()]
                    return Lines
            except:
                logger.error("Error in reading file {}".format(Path))
        else:
            logger.error("File does not exist")

    @staticmethod
    def checkIfFileExist(Path):
        if Path:
            return os.path.isfile(Path)
        else:
            return False
    
    @staticmethod
    def checkIfDir(dirPath):
        return os.path.isdir(dirPath)

    @staticmethod
    def ExcuteCommand(command):
        return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    @staticmethod
    def checkCommandResult(result):
        try:
            if result.returncode == 0:
                return True
            else:
                return False
        except:
            logger.error("command results doesn't have returecode")

    @staticmethod
    def writeToFile(FileName, Data):
        with open(FileName, "a") as file:
            if isinstance(Data, list):
                for i in Data:
                    file.write(i+'\n')
            elif isinstance(Data, str ):
                file.write(Data+'\n')
            else:
                logger.error("can't find the data Type ")

                
    @staticmethod
    def sendGetRequest(url, headers=None):
        if headers:
            return requests.get(url, headers=headers)
        else:
            return requests.get(url)

    @staticmethod
    def sendPostRequest():
        try:
            if self.headers and self.data and self.endpoint:
                response = requests.post(self.TargetUrl+self.endpoint, headers=self.headers, data=self.data ,proxies=proxies,verify=False)
                return response
            else:
                return False
        except:
            print("error in sending post")
            return False

    @staticmethod
    def chekcTool(tool):
        command = f"which {tool}"
        result = BaseClass.ExcuteCommand(command)
        if BaseClass.checkCommandResult(result):
            return True
        else:
            logger.error(f"This {tool} is not installed")
            return False

    @staticmethod
    def checkResponseResult(response):
        try:
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            logger.error("response doesn't have status_code")

    @staticmethod
    def checkResponseResult(response, text ):
        try:
            if response.status_code == 200 and text in response.text:
                return True
            else:
                return False
        except:
            print(f"error in finding {text} in response")

