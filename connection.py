import socket
from time import sleep
from threading import Thread
import asyncio

class client:

    HOST='192.168.0.190'
    PORT=40512
    
    def __init__(self):
        self.s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectToServer()
        pass
    
    def setupModuls(self, audio):
        self.audio=audio
    
    def getSelfObject(self):
        return self
    
    def run(self):
        micThread=Thread(target=self.comms,args=[])
        micThread.start()
        

    def connectToServer(self):
        try:
            self.s.connect((client.HOST,client.PORT))
        except socket.error as e:
            print(e)
    
    def sendToServer(self, data):
        my_bytes=bytes(data)
        
        self.s.send(my_bytes)

    def comms(self):
        while True:
            try:
                # Recive
                msg=self.s.recv(2048)

                asyncio.run(self.audio.sendToSpeackers(msg))
                
            except Exception as e:
                sleep(1)
                print(e)
                