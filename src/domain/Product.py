from decimal import Decimal, ROUND_HALF_UP

from src.domain.Category import Category

class Product(object):
    def __init__(self, name: str, price: Decimal, category: Category):
        self.name = name
        self.price = price
        self.category = category
      
    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def unitary_tax(self):
      return Decimal(self.price / Decimal(100) * self.category.get_tax_percentage()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def unitary_taxed_amount(self):
      return Decimal(self.price + self.unitary_tax()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
