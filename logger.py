import datetime
from abc import ABC, abstractmethod


class Log(ABC):
    @abstractmethod
    def __init__(self, file, module):
        pass

    @abstractmethod
    def log(self, msg):
        pass


class ConsoleLog(Log):
    def __init__(self, file, module):
        self.file = file
        self.module = module

    def log(self, msg):
        print(f"{datetime.datetime.now()}: {self.file}: {self.module}: {msg}")

# If we need any new type of logging like cloud based or something add that class here


class FileLog(Log):
    def __init__(self, file, module):
        self.file = file
        self.module = module

    def log(self, msg):
        with open("logs.txt", 'a') as file:
            file.write(msg)
            file.write("\n")


def get_log_obj(log_type, *args, **kwargs):
    if log_type.casefold() == "consolelog":
        return ConsoleLog(*args, **kwargs)
    elif log_type.casefold() == "filelog":
        return FileLog(*args, **kwargs)
    else:
        return None

