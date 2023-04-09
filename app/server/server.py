import socket
import sys
from threading import Thread

from app.server.config import ConfigServer
from app.logger import Logger


class MyProxy(ConfigServer):
    def __init__(self):
        super().__init__()
        self.make_proxy_server()
        self.LOG = Logger()




    def make_proxy_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(self.ADDR)
            print('Make Proxy Server -- Status OK !')
        except:
            print('ERROR: Cant create socket')
            sys.exit()

    def start(self):
        self.server.listen()
        print(f'[SERVER] Listening on: {self.IP} : {self.PORT}')
        if self.is_EVIL:
            print(f'[SERVER] EVIL PROXY adress: {self.EVIL_IP} : {self.EVIL_PORT}')
        
        try:
            print('[SERVER] Waiting for connections')
            while True:
                conn, addr = self.server.accept()
                hc = Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                hc.start()
        except KeyboardInterrupt:
            print('[SERVER] Server Stop !!!')
            self.server.close()
    
    def handle_client(self, conn, addr):
        print('[SERVER] New Connection From: ', addr[0])
        raw_msg = self.recive_msg(conn)
        self.LOG.log(raw_msg, ip=addr[0])
        msg = raw_msg.decode()
        config = []
        first = msg.split('\n')[0].split(' ')

        if first[0] == 'GET':
            config.append('GET')
        elif first[0] == 'CONNECT':
            config.append('CONNECT')
            config.append('CONNECT')
        else:
            config.append(None)
        print('HTTPS: ', first[1][0:5])
        if first[1][0:5] == 'https':
            config.append('https')
        elif first[1][0:4] == 'http' and first[1][4] == ':':
            config.append('http')
        else:
            config.append(None)
        print(config)
        target = self.unpack(config, first[1])
        print('TARGET: ', target)
        if target == False:
            print('[SERVER] Cant send msg ')
            return False
        
        
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            rs.connect(target)
            rs.sendall(raw_msg)
        except:
            self.LOG.log('Cant connect to server', target)
        
        response = self.recive_msg(rs)
        rs.close()
        # self.LOG.log(response, target)
        print('REPONSE FROM: ', target)
        print(response)
        conn.sendall(response)
        conn.close()










    def unpack(self, config, head_addr):
        print('CONFIG: ', config)
        if config[0] == None or config[1] == None:
            print('[SERVER] Unknown method ')
            return False

        if config[0] == 'CONNECT':
           
            slash = head_addr.find(':')
            address = head_addr[0:slash]
            port = head_addr[slash + 1:]
            return (address, int(port))
        
        else:
        
            temp = head_addr.replace(config[1] + '://', '')
            slash = temp.find('/')
            address = temp[0:slash]

            if config[1] == 'http':
                port = 80
            elif config[1] == 'https':
                port = 443
            else:
                return False

            return (address, port)

        





        



#########
PROXY = MyProxy()
PROXY.start()
