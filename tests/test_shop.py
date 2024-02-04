import pytest

from utils.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product: Product):
        assert product.check_quantity(10)
        assert not product.check_quantity(10001)

    def test_product_buy(self, product: Product):
        total_quantity = product.quantity
        product.buy(10)
        assert product.quantity == total_quantity - 10

    def test_product_buy_more_than_available(self, product: Product):
        with pytest.raises(ValueError):
            product.buy(10000)


class TestCart:

    def test_add_product(self, product: Product, cart: Cart):
        cart.add_product(product, 10)
        assert product in cart.products
        assert cart.products[product] == 10

    def test_add_additional_product(self, product: Product, cart: Cart):
        cart.add_product(product, 10)
        cart.add_product(product, 10)
        assert product in cart.products
        assert cart.products[product] == 20

    def test_add_essential_product(self, product: Product, cart: Cart):
        cart.add_product(product)
        assert product in cart.products
        assert cart.products[product] == 1

    def test_remove_product(self, product: Product, cart: Cart):
        cart.add_product(product, 6)
        cart.remove_product(product, 5)
        assert cart.products[product] == 1

    def test_remove_non_existent_product(self, product: Product, cart: Cart):
        with pytest.raises(ValueError):
            cart.remove_product(product, 8)

    def test_remove_none_product(self, product: Product, cart: Cart):
        cart.add_product(product)
        cart.remove_product(product, None)
        assert not cart.products

    def test_clear(self, product: Product, cart: Cart):
        cart.add_product(product, 10)
        cart.clear()
        assert not cart.products

    def test_get_total_price(self, product: Product, cart: Cart):
        cart.add_product(product, 10)
        assert cart.get_total_price() == 1000

    def test_buy(self, product: Product, cart: Cart):
        cart.add_product(product, 5)
        cart.buy()
        assert product.quantity == 995

    def test_buy_extra(self, product: Product, cart: Cart):
        with pytest.raises(ValueError):
            cart.add_product(product, 1001)
            cart.buy()
