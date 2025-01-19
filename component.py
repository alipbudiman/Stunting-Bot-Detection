from libs import *
from libs import EncryptAndDecryptAlgoritm as Enc
from libs import Bcolors

class AppComponents(Logger, CertantyFactor, Messager, Validation):
    def __init__(self) -> None:
        super().__init__()
        Config.__init__(self)
        Logger.__init__(self)
        
    
    