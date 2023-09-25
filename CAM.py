from Interfaces import UI

class CAM():
    
    def __init__(self, ui:UI):
        print("CAM init")
        ui.CAM_setter(self)

    