# Import necessary libraries
from kafka import KafkaConsumer
import json

# Function to process incoming messages
def process_message(message):
     # Assuming message is a list of transactions
    transactions = message
    
    # Minimum support threshold
    min_support = 0.5
    
    # Size of the sample
    sample_size = 1000
    
    # Number of partitions
    num_partitions = 4
    
    # Convert transactions to RDD
    rdd_transactions = spark.sparkContext.parallelize(transactions, num_partitions)
    
    # Take a sample of transactions
    sample_transactions = rdd_transactions.takeSample(False, sample_size)
    
    # Run first pass of SON algorithm to find candidate itemsets
    candidate_itemsets = generate_candidate_itemsets(rdd_transactions, min_support * sample_size / len(transactions), 2)
    
    # Count support for candidate itemsets
    support_counts = count_support(rdd_transactions, candidate_itemsets)
    
    # Filter frequent itemsets
    frequent_itemsets = [itemset for itemset, support in support_counts if support >= min_support * sample_size / len(transactions)]
    
    print("Frequent itemsets using SON algorithm:", frequent_itemsets)


# Kafka consumer configuration
kafka_servers = ['localhost:9092']  # Update with your Kafka broker(s) addresses
topic_name = 'test_topic11'  # Update with the Kafka topic name from which you want to consume messages

# Create Kafka consumer instance
consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_servers,
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

# Consume messages and process them
for message in consumer:
    process_message(message.value)

