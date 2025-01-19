class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class Logger:
    
    def __init__(self) -> None:
        pass
    
    def logger(self, data, color):
        if color not in Bcolors.__dict__.values():
            raise ValueError("Invalid color. Use a color from Bcolors class.")
        print("Logger:", f"{color}{data}{Bcolors.RESET}")