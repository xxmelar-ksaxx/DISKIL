from Interfaces import CAM

class UI:
    
    def __init__(self):
        print("UI init")

    def CAM_setter(self, CAM:CAM):
        self.CAM=CAM
        print("CAM setter -> UI")