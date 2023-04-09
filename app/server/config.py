from app.CONFIG import IP, PORT, LENGTH, EVIL_PROXY, EVIL_IP, EVIL_PORT
import sys



class ConfigServer:
    def __init__(self, evil=EVIL_PROXY):
        self.is_EVIL = False
        if evil == True:
            if EVIL_IP == '' or EVIL_PORT == None:
                print('Cant create Evil Proxy. Missing IP or PORT ')
                sys.exit()
            self.is_EVIL = True
            self.EVIL_IP = EVIL_IP
            self.EVIL_PORT = EVIL_PORT
            

        self.IP = IP
        self.PORT = PORT
        self.ADDR = (self.IP, self.PORT)
        self.LENGTH = LENGTH

    def recive_msg(self, conn):
        buff = b''
        while True:
            recv = conn.recv(self.LENGTH)
            buff += recv
            if len(recv) < self.LENGTH:
                break
        
        return buff
    
