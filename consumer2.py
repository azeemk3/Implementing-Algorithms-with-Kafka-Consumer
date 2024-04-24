# Import necessary libraries
from kafka import KafkaConsumer
import json
from collections import defaultdict

# Function to generate frequent itemsets of size k from candidate itemsets of size k
def generate_frequent_itemsets(candidate_itemsets, transactions, min_support):
    # Dictionary to store support count of each candidate itemset
    support_counts = defaultdict(int)
    # List to store frequent itemsets
    frequent_itemsets = []

    # Count support for each candidate itemset
    for itemset in candidate_itemsets:
        for transaction in transactions:
            if set(itemset).issubset(transaction):
                support_counts[tuple(itemset)] += 1

    # Filter itemsets that meet minimum support
    for itemset, support_count in support_counts.items():
        support = support_count / len(transactions)
        if support >= min_support:
            frequent_itemsets.append(itemset)

    return frequent_itemsets

# Function to generate candidate itemsets of size k+1 from frequent itemsets of size k
def generate_candidate_itemsets(frequent_itemsets, k):
    candidate_itemsets = []
    num_frequent_itemsets = len(frequent_itemsets)

    for i in range(num_frequent_itemsets):
        for j in range(i + 1, num_frequent_itemsets):
            itemset1 = frequent_itemsets[i]
            itemset2 = frequent_itemsets[j]
            if itemset1[:-1] == itemset2[:-1]:
                candidate_itemsets.append(sorted(list(set(itemset1) | set(itemset2))))

    return candidate_itemsets

# Function to generate frequent itemsets using PCY algorithm
def pcy_algorithm(transactions, min_support, hash_table_size):
    frequent_itemsets = []

    # Initialize frequent itemsets of size 1
    single_itemsets = [[item] for sublist in transactions for item in sublist]
    frequent_itemsets.extend(generate_frequent_itemsets(single_itemsets, transactions, min_support))

    k = 1
    while len(frequent_itemsets) > 0:
        k += 1
        candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, k)
        frequent_itemsets = generate_frequent_itemsets(candidate_itemsets, transactions, min_support)
        yield frequent_itemsets

# Function to process incoming messages using PCY algorithm
def process_message(message):
    # Assuming message is a list of transactions
    transactions = message
    
    # Minimum support threshold
    min_support = 0.5
    
    # Size of the hash table
    hash_table_size = 1000
    
    # Run PCY algorithm
    for frequent_itemsets in pcy_algorithm(transactions, min_support, hash_table_size):
        print("Frequent itemsets using PCY algorithm:", frequent_itemsets)

# Function to process incoming messages
def process_message(message):
    # Process the message here (e.g., implement PCY algorithm)
    # Print real-time insights and associations
    print("PCY algorithm implementation:", message)
    
# Kafka consumer configuration
kafka_servers = ['localhost:9092']  # Update with your Kafka broker(s) addresses
topic_name = 'test_topic11'  # Update with the Kafka topic name from which you want to consume messages

# Create Kafka consumer instance
consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_servers,
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

# Consume messages and process them
for message in consumer:
    process_message(message.value)

