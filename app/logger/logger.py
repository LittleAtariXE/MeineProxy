import os
import gzip
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
        if isinstance(msg, str):
            self.add_log(msg, ip)
        else:
            temp = self.extract_header(msg)
            if not temp:
                return 0
            self.add_log(temp, ip)
    
    def extract_header(self, msg):
        index = msg.find(b'\r\n\r\n')
        head = msg[0:index]
        try:
            head = head.decode()
            return head
        except:
            return None

    def add_log(self, msg, ip=None):
        if not ip:
            ip = 'Unknown Host'
        now = datetime.now()
        date_text = now.strftime("%d/%m/%Y %H:%M:%S")
        header = "-" * 100 + "\n" + f"----- {date_text} --------\n" + f"----From: {ip} -----\n" + "-" * 100 + "\n"
        header += msg + "\n\n\n\n"
        with open(self.LOG_FILE, 'a+') as f:
            f.write(header)



    def log2(self, msg, ip=None):
        if not isinstance(msg, str):
            if self.decode(msg) == None:
                msg = msg.decode()
                self.header(msg, ip)
                return 0
            elif self.decode(msg) == 'gzip':
                self.decode_gzip(msg, ip)
                return 0

            
    def decode_gzip(self, msg, ip=None):
        index = msg.find(b'\r\n\r\n')
        temp = msg[index:]

        try:
            decomp = gzip.decompress(temp[4:])
            decomp = decomp.decode()
            self.header(decomp, ip)
         
        except Exception as e:
            print('GZIP ERROR: ', e)

    def decode(self, msg):
        head = msg.find(b'\r\n\r\n')
        head = msg[0:head]

        head = head.decode()
        
        h_index = head.find('Content-Encoding:')
        if h_index == -1:
            return None
        
        index = head[h_index:].split()[1]
        index = index.strip()

        if index == 'gzip':
            return 'gzip'
        

        
        
        
    def header(self, msg, ip=None):
        if not ip:
            ip = "unknown adress"
        now = datetime.now()
        date_text = now.strftime("%d/%m/%Y %H:%M:%S")
        head = "-" * 100 + "\n" + f"----- {date_text} --- From: {ip}\n\n" + msg + "\n" + "-" * 100 + "\n"
        with open(self.LOG_FILE, 'a+') as f:
            f.write(head)

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
