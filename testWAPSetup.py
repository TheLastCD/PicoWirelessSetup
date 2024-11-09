from src.WAP import WAPSetup
from utils.jsonHandler import jsonHandler


test = WAPSetup("PicoWAP","12345678")

handler = jsonHandler()
try:
    
    response = test.WaitForPost()
    print(f"hashReceived = {response}")
    print(handler.HashHandler(response,"hash"))

    test.KillAP()
    print(handler.getFile("configMeta.json"))

except KeyboardInterrupt:
    test.KillAP()

