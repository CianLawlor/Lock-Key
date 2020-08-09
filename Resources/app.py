import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from PIL import Image, ImageTk
from tkinter import filedialog 

keyF = ""

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def write_key():
    print("Creating Key")
    encoding = 'utf-8'
    # Key Generation
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)
        global keyF
        keyF = key

def browse_files():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a file")
    if(filename != ""): 
        # Change label contents 
        #fileBrowse.configure(text="File Opened: "+filename)
        encryptListBox.insert(tk.END, filename)
        global fileF
        fileF = filename


def startEncrypt():
    encoding = 'utf-8'
    global keyF
    #print(encryptListBox.size)
    if(encryptListBox.size != 0 and keyF != ""):
        listBoxItems = encryptListBox.get(0, tk.END)
        for item in listBoxItems:
            print(item)
            encrypt(item, keyF)

def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        #read file
        file_data = file.read()

        #encrypt data
        encrypted_data = f.encrypt(file_data)
        with open(filename, "wb") as file:
            file.write(encrypted_data)
            print("Done")


def startDecrypt():
    encoding = 'utf-8'
    global keyF
    if(decryptListBox.size != 0 and keyF != ""):
        listBoxItems = decryptListBox.get(0, tk.END)
        for item in listBoxItems:
            try:
                decrypt(item, keyF)
            except InvalidToken:
                #print("Invalid Token")
                messagebox.showerror("Invalid Key", "Invalid Key Used To Decrypt File: \n" + item)


def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        #read file
        file_data = file.read()

        #decrypt data
        decrypted_data = f.decrypt(file_data)
        with open(filename, "wb") as file:
            file.write(decrypted_data)
            print("Done")

#Window Creation
window = tk.Tk()

#Window Attributes
window.title("Lock & Key")
window.geometry("400x260")
window.resizable(False, False)

def showAboutScreen():
    logoImage = Image.open(resource_path("icon.png"))
    photo = ImageTk.PhotoImage(logoImage)
    logoLabel = tk.Label(window, image = photo)
    logoLabel.image = photo
    logoLabel.place(height = 80, width = 80, x = 160, y = 20)

    aboutText = tk.Label(window, height = 100, width = 360,  text = "Lock & Key is a programme written by Cian Lawlor. \nThis prgramme encrypts and decrypts files for safe-keeping. \nThese files are encrypted/decrypted using \"keys\"\n which can be stored externally on USBs or online.\n\nContact: kurbee@protonmail.com")
    aboutText.place(height = 100, width = 360, x = 20, y = 130)

def showEncryptionScreen():
    widgetList = window.place_slaves()
    for item in widgetList:
        item.place_forget()

    #FileListBox
    eListBoxLabel = tk.Label(window, text = "Files to encrypt:")
    eListBoxLabel.place(width = 90, height = 20, x = 15, y = 50)
    encryptListBox = tk.Listbox(window)
    encryptListBox.place(width = 370, height = 120, x = 15, y = 70)

    #Buttons
    createKey = tk.Button(window, text = "Create Key", command = write_key)
    createKey.place(width = 80, x = 15, y = 15)

    findKey = tk.Button(window, text = "Find Key...", command = write_key)
    findKey.place(width = 80, x = 100, y = 15)

    fileBrowse = tk.Button(window, text = "Browse Files", command = browse_files)
    fileBrowse.place(width = 80,x = 15, y = 205)

    encryptFile = tk.Button(window, text = "Encrypt", command = startEncrypt)
    encryptFile.place(width = 80, x = 100, y = 205)   

    menubar.entryconfig(1, state = tk.DISABLED)
    menubar.entryconfig(2, state = tk.NORMAL)

def showDecryptionScreen():
    widgetList = window.place_slaves()
    for item in widgetList:
        item.place_forget()
        
    #FileListBox
    dListBoxLabel = tk.Label(window, text = "Files to decrypt:")
    dListBoxLabel.place(width = 90, height = 20, x = 15, y = 50)
    decryptListBox = tk.Listbox(window)
    decryptListBox.place(width = 370, height = 120, x = 15, y = 70)

    #Buttons
    findKey = tk.Button(window, text = "Find Key...", command = write_key)
    findKey.place(width = 80, x = 15, y = 15)

    fileBrowse = tk.Button(window, text = "Browse Files", command = browse_files)
    fileBrowse.place(width = 80,x = 15, y = 205)

    decryptFile = tk.Button(window, text = "Decrypt", command = startDecrypt)
    decryptFile.place(width = 80, x = 100, y = 205)   

    menubar.entryconfig(1, state = tk.NORMAL)  
    menubar.entryconfig(2, state = tk.DISABLED)    


#Window Contents
menubar = tk.Menu(window)
#mainmenu = tk.Menu(menubar, tearoff = 0)
menubar.add_command(label="Encrypt", command = showEncryptionScreen)
menubar.add_command(label="Decrypt", command = showDecryptionScreen)

window.config(menu = menubar)
showAboutScreen()
window.mainloop()