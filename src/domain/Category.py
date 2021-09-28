import decimal


class Category(object):
    def __init__(self, name:str, tax_percentage: decimal.Decimal):
        self.name = name
        self.tax_percentage = tax_percentage

    def get_name(self):
        return self.name

    def get_tax_percentage(self):
        return self.tax_percentage
