import pyfiglet
from colorama import Fore
def print_intro():
   
    styled_text=pyfiglet.figlet_format('FoxyNox',font= 'doom')
    print(Fore.BLUE + styled_text)