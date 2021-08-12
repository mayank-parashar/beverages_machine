import concurrent
from abc import ABC, abstractmethod
from concurrent.futures.thread import ThreadPoolExecutor

from logger import get_log_obj
import constants as const
from model import Status


class Strategy(ABC):
    @abstractmethod
    def run(self):
        pass


class RoundRobin(Strategy):
    def __init__(self, beverages, ingredient):
        self.beverages = beverages
        self.ingredient = ingredient

    def run(self):
        log = get_log_obj(const.CONSOLE_LOG, __name__, "Round Robin")
        log.log("start running test using Round Robin")
        not_available_count = 0
        beverage_count = len(self.beverages)
        while not_available_count < beverage_count:
            for beverage_name, beverage in self.beverages.items():
                if beverage.status == Status.NOT_AVAILABLE:
                    continue
                if beverage.create():
                    log.log(f"{beverage_name} is prepared")
                else:
                    log.log(f"{beverage_name} cannot be prepared because {beverage_name} is not available")
                    not_available_count += 1
        log.log("=" * 10 + "end" + "=" * 10)


class MultiThread(Strategy):
    def __init__(self, beverages, ingredient):
        self.beverages = beverages
        self.ingredient = ingredient

    @staticmethod
    def send_task(beverage):
        return beverage.create()

    def run(self):
        log = get_log_obj(const.CONSOLE_LOG, __name__, "MultiThread")
        log.log("start running test using MultiThread")
        not_available_count = 0  # Keep track of beverages for which ingredients are not available
        beverage_count = len(self.beverages)
        while not_available_count < beverage_count:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_name = {executor.submit(self.send_task, beverage): beverage_name for beverage_name, beverage in
                               self.beverages.items()}
                for future in concurrent.futures.as_completed(future_name):
                    beverage_name = future_name[future]
                    try:
                        result = future.result()
                        if result:
                            log.log(f"{beverage_name} is prepared")
                        else:
                            log.log(f"{beverage_name} cannot be prepared because {beverage_name} is not available")
                            not_available_count += 1
                    except Exception as exc:
                        log.log('%r generated an exception: %s' % (beverage_name, exc))

        log.log("=" * 10 + "end" + "=" * 10)


class Fair(Strategy):
    def __init__(self, beverages, ingredient):
        self.beverages = beverages
        self.ingredient = ingredient

    def run(self, ):
        # To be done
        raise NotImplementedError(self.__class__.__name__ + '.run')

# can create new test strategy class here


class StrategyAllocator:
    def __init__(self):
        # add new strategy class here
        self.mapper = {
            const.ROUND_ROBIN_STRATEGY: RoundRobin,
            const.FAIR_STRATEGY: Fair,
            const.MULTITHREAD: MultiThread
        }

    def get_strategy(self, strategy_name):
        return self.mapper.get(strategy_name.casefold(), None)
