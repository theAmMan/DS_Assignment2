class Topic: 
    #Required details in a single topic 
    def __init__(self, name: str) -> None:
        self._name = name
        self.producers = []
        self.consumers = []
        self.partitions = []
        self.current_round_robin_index = -1

    def add_producer(self, producer_id: int) -> None:
        self.producers.append(producer_id)

    def add_consumer(self, consumer_id: int) -> None: 
        self.consumers.append(consumer_id)

    def add_partition(self, partition_id: int) -> None: 
        self._partitions.append(partition_id)
        self._partitions.sort()

        if self.current_round_robin_index == -1:
            self.current_round_robin_index = 0

    def update_round_robin(self) -> None:
        self.current_round_robin_index = (self.current_round_robin_index + 1)%len(self.partitions)