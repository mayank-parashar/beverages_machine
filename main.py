import json

from logger import get_log_obj
from model import Ingredient, Beverages, BeverageIngredient
from test_strategy import StrategyAllocator
import constants as const


# populate
def populate_models(data):
    data = data.get("machine")
    ingredients = data.get("total_items_quantity")
    outlets_count = data.get("outlets", 0).get("count_n", 0)
    ingredient_map = dict()
    beverage_map = dict()

    for name, quantity in ingredients.items():
        ingredient_map[name] = Ingredient(name, quantity)

    beverages = data.get("beverages")
    for beverage_name, beverage_data in beverages.items():
        ingredient_list = list()
        for ingredient_name, ingredient_quantity in beverage_data.items():
            ingredient = ingredient_map.get(ingredient_name)
            if ingredient is None:
                ingredient_map[ingredient_name] = Ingredient(ingredient_name, 0)
                ingredient = ingredient_map.get(ingredient_name)
            ingredient_list.append(BeverageIngredient(ingredient, ingredient_quantity))
            ingredient.max = max(ingredient.max, ingredient_quantity)
        beverage_map[beverage_name] = Beverages(beverage_name, ingredient_list, outlets_count)

    return beverage_map, ingredient_map


if __name__ == '__main__':
    # Here you can select type of log you want condole or file
    log = get_log_obj(const.CONSOLE_LOG, __name__, "main")
    # reading input
    file = open("input.json")
    data = json.load(file)
    beverage_map, ingredient_map = populate_models(data)
    # select test strategy here
    strategy = StrategyAllocator().get_strategy(const.ROUND_ROBIN_STRATEGY)
    try:
        strategy(beverage_map, ingredient_map).run()
    except TypeError as tex:
        log.log("wrong strategy")
    except NotImplementedError:
        log.log("this strategy is yet to be implemented")
    except Exception as ex:
        log.log(f"some thing went wrong: {ex}")

    # checking if ingredient is at low indicator than refill it by 1000 else refill it by only 300
    for ingredient_name, ingredient in ingredient_map.items():
        if ingredient.low_indicator():
            ingredient.refill(1000)
        else:
            ingredient.refill(300)

    strategy = StrategyAllocator().get_strategy(const.MULTITHREAD)
    try:
        strategy(beverage_map, ingredient_map).run()
    except TypeError as tex:
        log.log("wrong strategy")
    except NotImplementedError:
        log.log("this strategy is yet to be implemented")
    except Exception as ex:
        log.log(f"some thing went wrong: {ex}")


