import os
from pathlib import Path

from datetime import datetime

LOG_FILE_NAME = 'logs'


BASE_DIR = str(Path(__file__).parent.parent.parent) + '/logs/'

class Logger:
    def __init__(self):
        self.BASE_DIR = BASE_DIR
        self._LOG_FILE_NAME = LOG_FILE_NAME
        self.make_file()


    
    def make_file(self):
        if not os.path.exists(self.BASE_DIR):
            os.makedirs(self.BASE_DIR)

        last = len(os.listdir(self.BASE_DIR)) + 1
        self.LOG_NAME = self._LOG_FILE_NAME + str(last) + '.txt'

        with open(self.BASE_DIR + self.LOG_NAME, 'w') as f:
            now = datetime.now()
            date_text = now.strftime("%d/%m/%Y %H:%M")
            text = f" ****** START NEW FILE ****** \n****** {date_text} ********\n" + "*" * 50 + "\n"
            f.write(text)

        self.LOG_FILE = self.BASE_DIR + self.LOG_NAME
    
    def log(self, msg, ip=None):
        if not isinstance(msg, str):
            try:
                msg = msg.decode()
                head = self.header(msg, ip)
            except:
                head = self.header_bin(msg, ip)

        
        with open(self.LOG_FILE, 'a+') as f:
            f.write(head)
        
        
        
    def header(self, msg, ip=None):
        if not ip:
            ip = "unknown adress"
        now = datetime.now()
        date_text = now.strftime("%d/%m/%Y %H:%M:%S")
        head = "-" * 50 + "\n" + f"----- {date_text} --- From: {ip}\n\n" + msg + "\n" + "-" * 50 + "\n"
        return head

    def header_bin(self, msg, ip=None):
        if not ip:
            ip = "unknown adress"
        now = datetime.now()
        date_text = now.strftime("%d/%m/%Y %H:%M:%S")
        head = "-" * 80 + f"\n ----- from: {ip}\n" + "-" * 80 + "\n"
        head = head.encode()
        head += msg
        return head







    


#######
