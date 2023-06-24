import pika
import json
import base64
# Store Username and Passwords for Rabbitmq
credentials = pika.PlainCredentials('asufhiwegn5', 'fioha7kasw')
# Create a connection
connection = pika.BlockingConnection(pika.ConnectionParameters('43.128.85.111',5672,'/',credentials))
# Create connection queue
ch = connection.channel()
def receive(ch, method, properties, body):
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

queue_name = 'algorithm_input_queue'
ch.basic_consume(queue=queue_name, on_message_callback=receive, auto_ack=False)

print('Waiting for messages. To exit press CTRL+C')
ch.start_consuming()


# Create a queue
#channel.queue_declare(queue='hello')

# Send a message
#channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

#Close the connection
#connection.close()

