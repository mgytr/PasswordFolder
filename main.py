from subprocess import getoutput
from sys import executable
from threading import Thread
from time import sleep
from os import path
from shutil import copy, make_archive



def loading(msg, torun, *args, **kwargs):
    thr = Thread(target=torun, args=args, kwargs=kwargs)
    thr.start()
    spin_states = ('|', '/', '-', '\\', '|')
    print(f'{msg}|          ', end='\r')
    while thr.is_alive():
        for state in spin_states:
            print(f'{msg}{state}          ', end='\r')
            sleep(0.08)

            

packages = [elem.split(' ')[0] for elem in getoutput(f'{executable} -m pip list').split('\n')]

if not 'colorama' in packages:
    print(f'ERROR: Colorama is not installed, installing...')
    loading('Installing Colorama ', getoutput, f'{executable} -m pip install colorama')
    from colorama import Fore
    print(f'{Fore.GREEN}SUCESS: Colorama is installed!{Fore.RESET}')
from colorama import Fore

if not 'pyinstaller' in packages:
    print(f'{Fore.RED}ERROR: {Fore.WHITE}PyInstaller is not installed, installing...{Fore.RESET}')
    loading('Installing PyInstaller ', getoutput, f'{executable} -m pip install pyinstaller')
    print(f'{Fore.GREEN}SUCESS: PyInstaller is installed!{Fore.RESET}')
if not 'cryptography' in packages:
    print(f'{Fore.RED}ERROR: {Fore.WHITE}Cryptography is not installed, installing...{Fore.RESET}')
    loading('Installing Cryptography ', getoutput, f'{executable} -m pip install cryptography')
    print(f'{Fore.GREEN}SUCESS: Cryptography is installed!{Fore.RESET}')

from cryptography.fernet import Fernet

class s:
    pass

key = s()
key.x = Fernet.generate_key()

folder = input(f'{Fore.YELLOW}Enter folder name (it should be in the running directory): {Fore.RESET}')


make_archive('archive', 'zip', f'./{folder}')
encarchive = Fernet(key.x).encrypt(open('archive.zip', 'rb').read())
open('archive.zip', 'wb').write(encarchive)
content = """
from cryptography.fernet import Fernet
from tkinter import *
from os import path, chdir
import zipfile
from io import BytesIO
from shutil import rmtree
from showinfm import show_in_file_manager

chdir(path.dirname(path.abspath(__file__)))

if not path.exists(f'{path.expanduser("~")}/.{NAMEFOLDER}') and not path.isdir(f'{path.expanduser("~")}/.{NAMEFOLDER}'):
    tk = Tk()
    menutk = Menu()
    tk.configure(menu=menutk)
    tk.geometry(f'300x150+{tk.winfo_pointerx()}+{tk.winfo_pointery()}')
    tk.title(f'Folder {NAMEFOLDER} is encrypted')

    def check():
        try:
            fernet = Fernet(key.get())
            unencrypt = fernet.decrypt(open('archive.zip', 'rb').read())
            io = BytesIO()
            io.write(unencrypt)

            file = zipfile.ZipFile(io)
            file.extractall(f'{path.expanduser("~")}/.{NAMEFOLDER}/')
            tk.quit()
            show_in_file_manager(f'{path.expanduser("~")}/.{NAMEFOLDER}')
            

        except:
            text.config(text='Incorrect key.')


    title = Label(text=f'Folder {NAMEFOLDER} is encrypted', font='"Open Sans" 19')
    title.pack(side='top', anchor=NW)

    key = Entry(font='"Open Sans" 13')
    key.pack(pady=2,anchor=NW, side=TOP)

    text = Label(text=f'', font='"Open Sans" 19')
    text.pack(pady=2,anchor=NW, side=TOP)



    btn = Button(text='Unlock', command=check)
    btn.pack(anchor=NW, side=TOP)


    tk.mainloop()

else:
    tk = Tk()
    menutk = Menu()
    def lock():
        rmtree(f'{path.expanduser("~")}/.{NAMEFOLDER}')
        tk.quit()
    tk.configure(menu=menutk)
    tk.geometry(f'450x150+{tk.winfo_pointerx()}+{tk.winfo_pointery()}')
    tk.title(f'Folder {NAMEFOLDER} is encrypted')
    title = Label(text=f'Folder {NAMEFOLDER} is encrypted, but is unlocked', font='"Open Sans" 19')
    title.pack(side='top', anchor=NW)



    btn = Button(text='Lock', command=lock)
    btn.pack(anchor=NW, side=TOP)
    tk.mainloop()
    """
open('archive.py', 'w').write(f'NAMEFOLDER = "{folder}"\n{content}')
loading('Compiling ', getoutput, f'{executable} -m PyInstaller --add-data "archive.zip:." -F -w archive.py')

copy('./dist/archive', './encfolder')

print(f'Your key is {key.x.decode()}. Save it.')
print(f'Move the file encfolder where you want.')