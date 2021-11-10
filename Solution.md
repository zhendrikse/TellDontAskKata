## Make [OrderItem.py](TellDontAskKata#src/domain/OrderItem.py) a [value object](https://medium.com/swlh/value-objects-to-the-rescue-28c563ad97c6)

Make [OrderItem.py](TellDontAskKata#src/domain/OrderItem.py) a value object and modify [OrderCreationUseCase.py](TellDontAskKata#src/useCase/OrderCreationUseCase.py) accordingly:

```python
class OrderItem(object):
  def __init__(self, product: Product, quantity: int, tax: Decimal, taxed_amount: Decimal):
    self.product = product
    self.quantity = quantity
    self.taxed_amount = taxed_amount
    self.tax = tax

  def get_product(self):
    return self.product

  def get_quantity(self):
    return self.quantity

  def get_taxed_amount(self):
    return self.taxed_amount
      
  def get_tax(self):
    return self.tax
```


## Make [Category.py](TellDontAskKata#src/domain/Category.py) a [value object](https://medium.com/swlh/value-objects-to-the-rescue-28c563ad97c6)

Make [Product.py](TellDontAskKata#src/domain/Product.py) a value object and modify [test_OrderCreationUseCase.py](TellDontAskKata#test/useCase/test_OrderCreationUseCase.py) accordingly:

```python
class Category(object):
  def __init__(self, name:str, tax_percentage: decimal.Decimal):
    self.name = name
    self.tax_percentage = tax_percentage

  def get_name(self):
    return self.name

  def get_tax_percentage(self):
    return self.tax_percentage
```

## Make [Product.py](TellDontAskKata#src/domain/Product.py) a [value object](https://medium.com/swlh/value-objects-to-the-rescue-28c563ad97c6)

Make [Product.py](TellDontAskKata#src/domain/Product.py) a value object and modify [test_OrderCreationUseCase.py](TellDontAskKata#test/useCase/test_OrderCreationUseCase.py) accordingly:

```python
class Product(object):
  def __init__(self, name: str, price: decimal.Decimal, category: Category):
    self.name = name
    self.price = price
    self.category = category
    
  def get_name(self):
    return self.name

  def get_price(self):
    return self.price

  def get_category(self):
    return self.category
```


## Remove setters from [Order.py](TellDontAskKata#src/domain/Order.py)

1. Move the approve logic from [OrderApprovalUseCase.py](TellDontAskKata#src/useCase/OrderApprovalUseCase.py) to [Order.py](TellDontAskKata#src/domain/Order.py) by first extracting the `request.is_approved()` into a separate variable and then using the extract-method refactoring:
  ```python
  def approve(self, isOrderApproved: bool):
        if self.status is OrderStatus.SHIPPED:
            raise ShippedOrdersCannotBeChangedError()

        if isOrderApproved and self.status is OrderStatus.REJECTED:
            raise RejectedOrderCannotBeApprovedError()

        if not isOrderApproved and self.status is OrderStatus.APPROVED:
            raise ApprovedOrderCannotBeRejectedError()

        self.status = OrderStatus.APPROVED if isOrderApproved else OrderStatus.REJECTED  
  ```

2. Extract reject logic from approve method in [Order.py](TellDontAskKata#src/domain/Order.py)

  ```python
  def approve(self):
      if self.status is OrderStatus.SHIPPED:
          raise ShippedOrdersCannotBeChangedError()

      if self.status is OrderStatus.REJECTED:
          raise RejectedOrderCannotBeApprovedError()

      self.status = OrderStatus.APPROVED

  def reject(self):
      if self.status is OrderStatus.SHIPPED:
          raise ShippedOrdersCannotBeChangedError()
          
      if self.status is OrderStatus.APPROVED:
          raise ApprovedOrderCannotBeRejectedError()

      self.status = OrderStatus.REJECTED
  ```

3. Create order constructor in [Order.py](TellDontAskKata#src/domain/Order.py):
  ```python
  def __init__(self, order_id:int = 1, currency:str = "EUR"):
      self.status = OrderStatus.CREATED
      self.items= []
      self.currency= "EUR"
      self.total = Decimal("0.00")
      self.tax = Decimal("0.00")
      self.id = order_id  
  ```
  and use it in [OrderCreationUseCase.py](TellDontAskKata#src/useCase/OrderCreationUseCase.py) and _all_ test cases. The `set_id()` can now be removed from [Order.py](TellDontAskKata#src/domain/Order.py).

  Finally, the constructor argument `order_id:int = 1` can be changed to `order_id:int`.

4. Create shipping methods in [Order.py](TellDontAskKata#src/domain/Order.py)
  ```python
  def check_shipment(self):
    if self.status is OrderStatus.CREATED or self.status is OrderStatus.REJECTED:
      raise OrderCannotBeShippedError()

    if self.status is OrderStatus.SHIPPED:
      raise OrderCannotBeShippedTwiceError()

  def shipped(self):
    self.status = OrderStatus.SHIPPED
  ```
  so that [OrderShipmentUseCase.py](TellDontAskKata#src/useCase/OrderShipmentUseCase.py) becomes:
  ```python
order.check_shipment()
  self.shipment_service.ship(order)
  order.shipped()
  self.order_repository.save(order)
  ```

5. Remove all the `set_status()` calls from [test_OrderApprovalUseCase.py](TellDontAskKata#test/useCase/test_OrderApprovalUseCase.py). The `OrderStatus.CREATED` can be removed, the rejected and shipped orders have to be created by mimicing the workflow from approved to shipped like so:
  ```python
  shipped_order = Order()
  shipped_order.set_id(1)
  shipped_order.approve()
  shipped_order.shipped() 
  ```
  Do the same with [test_OrderShipmentUseCase.py](TellDontAskKata#test/useCase/test_OrderShipmentUseCase.py). Finally, remove the `set_status()` from [Order.py](TellDontAskKata#src/domain/Order.py).


6. Remove `set_items()` in [Order.py](TellDontAskKata#src/domain/Order.py)
  
  - Create an `add_order_item()` method in [Order.py](TellDontAskKata#src/domain/Order.py):

    ```python
    def add_order_item(self, item: OrderItem):
      self.items.append(item)
      self.total = self.total + item.get_taxed_amount()
      self.tax= self.tax + item.get_tax()  
    ```  
    and use it in the [OrderCreationUseCase](TellDontAskKata#src/useCase/OrderCreationUseCase.py).

  - Create the following methods in [Product.py](TellDontAskKata#src/domain/Product.py):

    ```python
    def unitary_tax(self):
      return Decimal(self.price / Decimal(100) * self.category.get_tax_percentage()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def unitary_taxed_amount(self):
      return Decimal(self.price + self.unitary_tax()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    ```

  - Next, in [OrderItem.py](TellDontAskKata#src/domain/OrderItem.py) modify the constructor like so:

    ```python
    def __init__(self, product: Product, quantity: int):
      self.product = product
      self.quantity = quantity
      self.taxed_amount = Decimal(self.product.unitary_taxed_amount() * Decimal(quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
      self.tax = self.product.unitary_tax() * (Decimal(quantity))
    ```
  
    The `run()` method in [OrderCreationUseCase.py](TellDontAskKata#src/useCase/OrderCreationUseCase.py) now simplifies to:
    ```python
    def run(self, request: SellItemsRequest):
      order = Order("EUR")

      for item_request in request.get_requests():
        product = self.product_catalog.get_by_name(item_request.get_product_name())

        if product is None:
          raise UnknownProductError()
        else:
          order.add_order_item(OrderItem(product, item_request.get_quantity()))
    ``` 
    The tax arguments can now be removed from the `OrderItem` constructor.

  - Finally, the `set_items()`, `set_currency()`, `set_total()`, and `set_tax()` can be removed from [Order.py](TellDontAskKata#src/domain/Order.py).

  7. Use Python [data classes](https://towardsdatascience.com/9-reasons-why-you-should-start-using-python-dataclasses-98271adadc66) for the implementation of the value objects such as the [Category](TellDontAskKata#src/domain/Category.py):

  ```python
  import decimal
  from dataclasses import dataclass

  @dataclass(frozen = True)
  class Category(object):
    name: str
    tax_percentage: decimal.Decimal
  ``` 
