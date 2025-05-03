class ErrorCollector:
    def __init__(self):
        self.errors = []

    def add(self, error, type):
        self.errors.append(f"{error} type={type}")
