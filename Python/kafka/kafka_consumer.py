from kafka import KafkaConsumer
from kafka import OffsetAndMetadata
from kafka import TopicPartition

import logging
logger = logging.getLogger(__name__)

# CONFIG (can be moved to .env file)
KAFKA_TOPIC = "my-topic"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_GROUP_ID = "my-group"
KAFKA_MAX_POLL_INTERVAL_MS = 900000
KAFKA_MAX_POLL_RECORDS = 5

def process_message(message):
    pass

def main():
    # Create Kafka consumer instance
    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                             group_id=KAFKA_GROUP_ID,
                             auto_offset_reset='earliest',
                             enable_auto_commit=False,
                             max_poll_interval_ms=KAFKA_MAX_POLL_INTERVAL_MS,
                             max_poll_records=KAFKA_MAX_POLL_RECORDS,
                             value_deserializer=lambda x: x.decode('utf-8'))


    # Continuously consume and process messages
    try:
        for message in consumer:
            logging.info("Received message: %s", message.value)
            process_message(message)
            # consumer.commit()
            consumer.commit(offsets={TopicPartition(message.topic, message.partition): OffsetAndMetadata(message.offset + 1, None)})

    except KeyboardInterrupt:
        pass
    finally:
        # Close the consumer and database session when done
        consumer.close()
        logging.info("Consumer closed")
        
if __name__ == "__main__":
    main()