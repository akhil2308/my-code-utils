import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

logger = logging.getLogger(__name__)


class Producer:
    def __init__(self, topic_name, bootstrap_servers):
        self.topic_name             = topic_name
        self.bootstrap_servers      = [x.strip() for x in bootstrap_servers.split(',')]
        self.producer               = KafkaProducer(
                                                    bootstrap_servers=self.bootstrap_servers,
                                                    value_serializer=lambda x:json.dumps(x).encode('utf-8'))

    def send_message(self, data):
        logger.info("producing message %s for topic %s", data, self.topic_name)
        ret = self.producer.send(self.topic_name, value=data)
        self.producer.flush()
            
    def send_bulk_records(self,record):
        count = 0
        for data in record:
            ret = self.producer.send(self.topic_name, value=data)
            count += 1
            
            if count%10000 == 0:
                logger.info("no of records sent to kafka topic {} = {}".format(self.topic_name,count))
                
        self.producer.flush()      
        logger.info("total no of records sent to kafka topic {} = {}".format(self.topic_name,count))