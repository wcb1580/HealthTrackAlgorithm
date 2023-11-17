import time

import pika
import json

from pika.exceptions import AMQPConnectionError

from Algorithm import predict_disease

"Receive the message from RabbitMQ and provide a response to it"


class RabbitMQReceiver:
    def __init__(self, channel, queuename):
        self.channel = channel
        self.queuename = queuename

    def reconnect(self):
        # Wait before trying to reconnect
        time.sleep(5)  # 5 seconds delay, adjust as needed
        # Attempt to reconnect
        while True:
            try:
                # Assuming you have a method to create and return a new channel
                self.channel = self.create_channel()
                self.Start_receiving()
                break
            except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError) as e:
                print("Failed to reconnect to RabbitMQ:", e)
                time.sleep(5)  # Wait for 5 seconds before trying again

    def Receive(self, ch, method, properties, body):
        try:
            message = body.decode('utf-8')
        except UnicodeDecodeError:
            print("body is not a valid UTF-8 encoded string")
            return
        if message:
            try:
                message = json.loads(body)
                print(message)
                data = self.Propose_data(message)
                # Process the message and prepare a response
                # Convert the response to a JSON string
                response = json.dumps(data)
                # Construct received correlation_id
                prop = pika.BasicProperties(correlation_id=properties.correlation_id)
                # Send the response back to RabbitMQ
                routing_key = str(properties.reply_to)
                ch.basic_publish(exchange='', routing_key=routing_key, properties=prop, body=response)
                print(response)

                ch.basic_ack(delivery_tag=method.delivery_tag)
            except json.JSONDecodeError:
                print("Decoding JSON has failed")
                ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            print("Message is empty")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def Propose_data(self, message):
        # Provide predicted diseases with relevant probability
        symptoms = message['symptoms']
        data = predict_disease(symptoms)

        return data

    def Start_receiving(self):
        try:
            self.channel.queue_declare(queue=self.queuename, durable=True)
            self.channel.basic_consume(queue=self.queuename, on_message_callback=self.Receive, auto_ack=False)
            self.channel.start_consuming()
        except (AMQPConnectionError, pika.exceptions.AMQPChannelError) as e:
            print("Connection lost:", e)
            self.reconnect()

    def create_connection(self):
        """Create a new RabbitMQ connection and channel."""
        try:
            # Assuming that 'pika.ConnectionParameters()' is set up according to your RabbitMQ configuration
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queuename, durable=True)
        except AMQPConnectionError as e:
            print("Failed to create a RabbitMQ connection:", e)
            time.sleep(5)  # Wait for 5 seconds before trying again
            self.create_connection()