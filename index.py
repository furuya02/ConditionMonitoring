from mqtt import Mqtt
from logger import Logger
import time
import json

class Job():
    def __init__(self, commandList):
        self.__commandList = commandList

        config = json.load(open('./config.json', 'r'))

        logFile = "./log/{}".format(config["appName"])
        logger = Logger(config["appName"], config["logLevel"], filename=logFile)

        port = 8883
        self.__topic = config["topic"]
        self.__mqtt = Mqtt(logger, config["endPoint"], port, config["rootCA"], config["certificate"], config["privateKey"], config["clientId"])
        self.__mqtt.subscribe(self.__topic + "/Request", self.__callback)
        
        self.__result = None

        self.__loop()

    def __callback(self, client, userdata, message):
        print(self)
        p = json.loads(message.payload)
        if("command" in p):
            command = p["command"]
            param = None
            if("param" in p):
                param = p["param"]
            for key in self.__commandList.keys():
                if(command == key):
                    self.__result = self.__commandList[key](param)
                    return

    def __loop(self):
        while True:
            time.sleep(0.5)

            if(self.__result is None):
                continue
            payload = {
                "message": self.__result   
            }
            self.__result = None
            self.__mqtt.publish(self.__topic + "/Response", json.dumps(payload))


# コマンドと処理を定義
def Shutdown(param):
    print("> Shutdown")
    return "system is going down for system halt NOW!"

def Reboot(param):
    print("> Reboot")
    return "The system is going down for reboot NOW!"

def Echo(param):
    print("> Echo {}".format(param))
    return param

commandList = {
    "shutdown": Shutdown,
    "reboot": Reboot,
    "echo": Echo
}

# メイン処理
job = Job(commandList)
