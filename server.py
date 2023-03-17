import socket
from threading import Thread
from time import sleep
from os import system

class p:


    users={}

    HOST='0.0.0.0'
    PORT=40512


    def __init__(self):
        self.server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((p.HOST, p.PORT))
        self.server.listen(5)

        self.t1=Thread(target=self.run, args=[])
        self.t1.start()

        self.statusThread=Thread(target=p.statusTarget, args=[])
        self.statusThread.start()


    def run(self):
        while True:
            print(".")
            try:
                cs, addr = self.server.accept()
                cs.send(bytes("You connected !!","utf-8"))
                uip=addr[0]+str(addr[1])
                p.addNewUser(cs, uip)
                p.serverStatus(f"Accept from -> {addr}")
                t=Thread(target=p.handleClient, args=[cs, addr, uip])
                t.start()
            except Exception as e:
                print('Err !?!')
                print(e)
    
    def addNewUser(cs, uip):
        try:
            p.users.update({uip:cs})
        except:
            pass
    
    def removeUser(uip):
        try:
            p.users.pop(uip)
        except:
            pass
    
    def notifyAllClients(msg):
        for k, v in p.users.items():
            v.send(msg)
    
    def sendToUsers(cs, addr, uip):
        while True:
            try:
                msg=cs.recv(2048)
                for k, v in p.users.items():
                    # send to all users except me
                    if k != uip:
                        v.send(msg)
            except Exception as e:
                p.removeUser(uip)
                p.serverStatus(f'Disconnected :{addr}')
                break
    
    def handleClient(cs, addr, uip):
        p.sendToUsers(cs, addr, uip)

    def serverStatus(msg):
        p.clearTerminal()
        print(msg)
        print(p.users.keys())
    
    def statusTarget():
        while True:
            sleep(1)
            p.clearTerminal()
            print((p.users.keys()))

    def clearTerminal():
        try:
            system('cls') # Win
        except:
            system('clear') # Others

p()