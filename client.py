from audio import audio
from connection import client

class CM:

    def __init__(self):
        # 1- create and initialize objects
        self.audio = audio()
        self.client = client()

        # 2- inject dependencies
        self.audio.setupModuls(self.client.getSelfObject())
        self.client.setupModuls(self.audio.getSelfObject())

        # 3- run services
        self.audio.run()
        self.client.run()

CM()


    



