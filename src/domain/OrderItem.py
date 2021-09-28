from decimal import Decimal, ROUND_HALF_UP

from src.domain.Product import Product

class OrderItem(object):
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.taxed_amount = Decimal(self.product.unitary_taxed_amount() * Decimal(quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        self.tax = self.product.unitary_tax() * (Decimal(quantity))


    def get_product(self):
        return self.product

    def get_quantity(self):
        return self.quantity

    def get_taxed_amount(self):
        return self.taxed_amount
        
    def get_tax(self):
        return self.tax
