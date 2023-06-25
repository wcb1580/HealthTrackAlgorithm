import pika
"The file constructs a connection to the RabbitMQ protol"
class RabbitMQConnection:
    def __init__(self, username, password, host, port, vhost):
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, vhost, self.credentials))
        self.channel = self.connection.channel()

    def get_channel(self):
        return self.channel

    def close_connection(self):
        self.connection.close()