class Topic: 
    #Required details in a single topic 
    def __init__(self, name: str) -> None:
        self._name = name
        self.producers = []
        self.consumers = []
        self.partitions = [1]

    def add_producer(self, producer_id: int) -> None:
        self.producers.append(producer_id)

    def add_consumer(self, consumer_id: int) -> None: 
        self.consumers.append(consumer_id)

    def add_partition(self, partition_id: int) -> None: 
        self._partitions.append(partition_id)
