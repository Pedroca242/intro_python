import paho.mqtt.client as mqtt
import logging

class MQTTCommunicator:
    def __init__(self, client_id, broker_address, port=1883):
        self.client_id = client_id
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client(client_id)
        self.connected_clients = []
        self.info = []

        # Configura os callbacks
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

        # Inicia a conexão com o broker MQTT
        self.client.connect(self.broker_address, self.port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == mqtt.MQTT_ERR_SUCCESS:
            logging.info("Conectado ao broker MQTT")
            self.connected_clients.append(client._client_id)
        else:
            logging.error(f"Falha na conexão ao broker MQTT com código de retorno: {rc}")

    def on_publish(self, client, userdata, mid):
        logging.info("Mensagem publicada")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logging.info(f"Inscrito no tópico com QoS {granted_qos}")

    def on_message(self, client, userdata, msg):
        mensagem = msg.payload.decode()
        logging.info(f"Recebido no tópico '{msg.topic}': {mensagem}")
        self.info = mensagem

    def publish(self, topic, message, qos=0):
        self.client.publish(topic, message, qos=qos)

    def subscribe(self, topic, qos=0):
        self.client.subscribe(topic, qos=qos)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()