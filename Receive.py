import pika
import json
from Algorithm import predict_disease
"Receive the message from RabbitMQ and provide a response to it"
class RabbitMQReceiver:
    def __init__(self, channel, queuename):
        self.channel = channel
        self.queuename = queuename
    def Receive(self, ch, method, properties, body):
        try:
            message = body.decode('utf-8')
        except UnicodeDecodeError:
            print("body is not a valid UTF-8 encoded string")
            return
        if message:
            try:
                message = json.loads(body)
                data = self.Propose_data(message)
                # Process the message and prepare a response
                #Convert the response to a JSON string
                response = json.dumps(data)
                # Construct received coorelation_id
                prop=pika.BasicProperties(correlation_id=properties.correlation_id)
                # Send the response back to RabbitMQ
                routing_key = str(properties.reply_to)
                ch.basic_publish(exchange='', routing_key=routing_key, properties=prop, body=response)
            except json.JSONDecodeError:
                print("Decoding JSON has failed")
        else:
            print("Message is empty")
    def Propose_data(self, message):
        #Provide prodicted diseases with relevant probability
        symptoms = message['symptoms']
        data = predict_disease(symptoms)

        return data

    def Start_receiving(self):
        self.channel.basic_consume(queue=self.queuename, on_message_callback=self.Receive, auto_ack=False)
        self.channel.start_consuming()