from plugin_system.base_device import OSAInterface
import pyvisa

plugin_info = {
    "name": "Agilent 86142 OSA",
    "type": "osa",
    "class": "OSA_86142"
}

class OSA_86142(OSAInterface):
    @classmethod
    def can_connect(cls):
        rm = pyvisa.ResourceManager()
        res = rm.list_resources()
        for i in res:
            try:
                print(f"Trying resource: {i}")
                inst = rm.open_resource(i)
                idn = inst.query("*IDN?")
                if "86142" in idn:
                    return inst
            except:
                continue
        return None
    
    def __init__(self, inst):
        self.inst = inst

    def connect(self):
        self.inst.write("*RST")