"""
MQTT pub/subの基本クラス
"""

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

class Mqtt():
    def __init__(self, logger, endPoint, port, rootCA, certificate, privateKey, clientId):
        self.__logger = logger
        self.__logger.debug("Mqtt.__init__()")
        self.__client = AWSIoTMQTTClient(clientId)
        self.__client.configureEndpoint(endPoint, port)
        self.__client.configureCredentials(rootCA, privateKey, certificate)
        self.__client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.__client.configureOfflinePublishQueueing(-1)
        self.__client.configureDrainingFrequency(2)
        self.__client.configureConnectDisconnectTimeout(10)
        self.__client.configureMQTTOperationTimeout(5)
        self.__client.connect()
    
    def subscribe(self, topic, callback):
        self.__logger.debug("Mqtt.subscribe()")
        self.__client.subscribe(topic, 1, callback)

    def publish(self, topic, payload):
        self.__client.publish(topic, payload, 1)

