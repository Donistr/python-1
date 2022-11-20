from t_4 import next


class DataIterator:
    def __init__(self, limit):
        self.limit = limit
        self.counter = 0

    def __next__(self, data_file_name: str = 'data_file.csv'):
        if self.counter < self.limit:
            self.counter += 1
            return next(self.counter, data_file_name)
        else:
            raise StopIteration
