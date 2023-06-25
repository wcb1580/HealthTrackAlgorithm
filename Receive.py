import pika
"The file receive the message from RabbitMQ and provide a response to it"
class RabbitMQReceiver:
    def __init__(self, channel, queuename):
        self.channel = channel
        self.queuename = queuename
    def Receive(self, ch, method, properties, body):
        message = body.decode()
        print("Received %r" % message)
        # Process the message and prepare a response
        response = 'Received'
        # Convert the response to a JSON string
        #response_json = json.dumps(response)

        # Construct received coorelation_id
        prop=pika.BasicProperties(correlation_id=properties.correlation_id)
        # Send the response back to RabbitMQ
        ch.basic_publish(exchange='', routing_key=properties.reply_to, properties=prop, body=response.encode('utf-8'))
    def Start_receiving(self):
        self.channel.basic_consume(queue=self.queuename, on_message_callback=self.Receive, auto_ack=False)
        print('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()