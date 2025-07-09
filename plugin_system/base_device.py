from abc import ABC, abstractmethod

class OSAInterface(ABC):
    @abstractmethod
    def connect(self): pass
    @abstractmethod
    def set_start_wvl(self, start_wvl: float): pass
    @abstractmethod
    def set_stop_wvl(self, stop_wvl: float): pass
    @abstractmethod
    def set_center_wvl(self, center_wvl: float): pass
    @abstractmethod
    def set_span(self,span: float): pass
    @abstractmethod
    def set_sweep_mode(self, mode: str): pass
    @abstractmethod
    def start_sweep(self): pass
    @abstractmethod
    def set_sesitivity(self, sensitivity: float): pass
    @abstractmethod
    def set_resolution_bw(sefl, bandwidth: float): pass

class CLIInterface(ABC):
    @abstractmethod
    def connect(self): pass
    @abstractmethod
    def write_reg(self,reg: str,data: str): pass
    @abstractmethod
    def read_reg(self,reg: str): pass