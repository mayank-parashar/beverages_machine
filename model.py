from enum import Enum


class Status(Enum):
    AVAILABLE = 0
    NOT_AVAILABLE = 1


class Ingredient:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity
        self.max = 0

    def refill(self, quantity):
        self.quantity += quantity

    def low_indicator(self):
        # Logic for low indicator is if this ingredient is not have sufficient quantity to make atleast one quantity
        # of any beverage than it is low
        if self.quantity < self.max:
            return True
        return False


class BeverageIngredient:
    def __init__(self, ingredient, quantity):
        self.ingredient = ingredient
        self.quantity = quantity


class Beverages:
    def __init__(self, name, ingredient, outlets_count):
        self.beverage_ingredient_list = ingredient
        self.status = Status.AVAILABLE
        self.name = name
        self.current_locks = 0
        self.max_locks = outlets_count

    def is_outlet_available(self):
        if self.current_locks <= self.max_locks:
            return True
        return False

    def create(self):
        if self.__have():
            for each_ingredient in self.beverage_ingredient_list:
                beverage_ingredient = each_ingredient
                ingredient = each_ingredient.ingredient
                ingredient.quantity = ingredient.quantity - beverage_ingredient.quantity
            self.current_locks -= 1  # Lock is removed on this ingredient
            return True
        else:
            return False

    def __have(self):
        # check if this beverage can be possible and also take lock on ingredient
        for each_ingredient in self.beverage_ingredient_list:
            beverage_ingredient = each_ingredient
            ingredient = each_ingredient.ingredient
            if ingredient.quantity < beverage_ingredient.quantity:
                self.status = Status.NOT_AVAILABLE
                return False
        self.status = Status.AVAILABLE
        if self.is_outlet_available():
            self.current_locks += 1
        else:
            return False
        return True
