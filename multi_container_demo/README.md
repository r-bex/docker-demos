### Multiple container demo

Containers:
- one to run a Kafka broker. No code, directly pulls `spotify/kafka` image
- one to run a process that will constantly send dummy data into a Kafka topic = `data` directory
- one to run our actual task, the model prediction = `predictor` directory