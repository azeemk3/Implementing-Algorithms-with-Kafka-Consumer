from kafka import KafkaProducer
import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        data = [json.loads(line.strip()) for line in lines]
    return data

# Kafka producer configuration
kafka_servers = ['localhost:9092']  # Update with your Kafka broker(s) addresses
topic_name = 'test_topic11'

producer = KafkaProducer(bootstrap_servers=kafka_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Read data from JSON file
json_data = read_json_file('preprocessed_data.json')

# Send data to Kafka topic
for item in json_data:
    producer.send(topic_name, value=item)
    print("Sent: ", item)

# Close producer
producer.close()
