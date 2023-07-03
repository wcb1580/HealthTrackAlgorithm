# HealthTrackAlgorithm

This Python application serves as a robust conduit for information processing and predictive analysis, acting in tandem with our Spring Boot application server. The architecture is structured to enable seamless exchange of user input data between these two applications, facilitated by the reliable message broker RabbitMQ.


## What does it do:

When a user provides their symptoms via the Spring Boot application, these data points are processed and sent to the Python application through RabbitMQ's robust communication channels. Within the Python application, a sophisticated machine learning model is put to work. This model has been trained on a vast array of data, enabling it to provide accurate predictions about a person's likelihood of developing any one of 41 different popular diseases.


## Insights:

Thus, our Python application effectively bridges the gap between user input and data science, delivering predictive insights that are critical in preemptive health management. By harnessing the capabilities of machine learning and the reliability of RabbitMQ, the application transforms symptom data into actionable health information.



### Connection.py: 

- Construct connection between python to RabbitMQ


### Receive.py: 

- Receive message from RabbitMQ and provide response
### Skelton.py: 

- Execution file
### Algorithm.py:

- Machine Learning Model
