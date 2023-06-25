from Connection import RabbitMQConnection
from Receive import RabbitMQReceiver

def main():
    ch = RabbitMQConnection('asufhiwegn5', 'fioha7kasw', '43.128.85.111', 5672, '/')
    receiver = RabbitMQReceiver(ch.get_channel(), 'algorithm_input_queue')
    receiver.Start_receiving()

if __name__ == "__main__":
    main()


# Create a queue
#channel.queue_declare(queue='hello')

# Send a message
#channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

#Close the connection
#connection.close()

