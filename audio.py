from time import sleep
import numpy as np
import pyaudio
from threading import Thread
from os import system
import noisereduce as nr

class audio:

    CHUNK = 2024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44000
    p = pyaudio.PyAudio()

    def __init__(self):
        self.stream=self.Stream()
        self.VOLUME=1
        self.SENSITY=100  
        self.MUTE=False
        self.SR=150_000   # filter value
        self.NR=100       # noise rediction filter
    
    def setupModuls(self, client):
        self.client=client
    
    def getSelfObject(self):
        return self
    
    def run(self):
        micThread=Thread(target=self.runLoop,args=[])
        micThread.start()
        sleep(1.5)
        mnueThread=Thread(target=self.mnue,args=[])
        mnueThread.start()

    def Stream(self):
        stream = audio.p.open(format=audio.FORMAT,
                channels=audio.CHANNELS,
                rate=audio.RATE,
                input=True,
                output=True,
                frames_per_buffer=audio.CHUNK)
        return stream

    def runLoop(self):
        while True:
            streamData=self.stream.read(audio.CHUNK)
            data = np.frombuffer(streamData, dtype=np.int16)
            reduced_noise = nr.reduce_noise(y=data, sr=self.SR,thresh_n_mult_nonstationary=self.NR) 

            micMax=max(reduced_noise)
            micMin=min(reduced_noise)

            if(micMax>self.SENSITY and micMin<-self.SENSITY and not self.MUTE):
                self.sendData(bytes(reduced_noise))
    
    def sendData(self, data):
        if len(data)>=4096:

            self.client.sendToServer(data)
    
    async def sendToSpeackers(self, data):
        data=np.frombuffer(data, dtype=np.int16)
        
        self.stream.write((data*self.VOLUME).tobytes())
    
    def mnue(self):
        opt={
            'v':'1- V+ , 2- V-',
            's':'3- S+ , 4- S-',
            'sr':'5- SR+ , 6- SR-',
            'nr':'7- NR+ , 8- NR-',
            'm':'9- Is Mute? ',
        }

        while True:
            system('cls')
            print(f"Volume: {self.VOLUME}") 
            print(f"Sensivity: {self.SENSITY}")
            print(f"SR: {self.SR}")
            print(f"NR: {self.NR}") 
            option=input(f"{opt['v']}\n{opt['s']}\n{opt['sr']}\n{opt['nr']}\n{opt['m']} ({self.MUTE})")
            self.clearTerminal()
            if option=='1':
                self.VOLUME+=1
            elif option=='2':
                if self.VOLUME !=0:
                    self.VOLUME-=1
            elif option=='3':
                self.SENSITY+=10
            elif option=='4':
                self.SENSITY-=10
            elif option=='5':
                self.srUP()
            elif option=='6':
                self.srDown()
            elif option=='7':
                self.nrUP()
            elif option=='8':
                self.nrDown()
            elif option=='9':
                if self.MUTE:
                    self.MUTE=False
                else:
                    self.MUTE=True
    
    def clearTerminal(self):
        try:
            system('cls') # Win
        except:
            system('clear') # Others

    #-----------------
    # Audio filter stuff
    def srUP(self):
        if self.SR<250000:
            self.SR+=10_000
    def srDown(self):
        if self.SR>110000:
            self.SR-=10_000
    def nrUP(self):
        if self.NR<400:
            self.NR+=10
    def nrDown(self):
        if self.NR>10:
            self.NR-=10

