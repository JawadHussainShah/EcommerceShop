from django import template

register = template.Library()
@register.filter(name = 'IsInCart')
def is_in_cart(product, cart):
    keys = cart.keys()
    # print(keys,product.id)
    for id in keys:
        if int(id)==product.id:
            # print(keys,[]+[product.id])
            return True
    return False

@register.filter(name = 'item_count')
def item_count(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id)==product.id:
            return cart.get(id)
    return 0

@register.filter(name = 'total_price')
def total_price(product, cart):
    return product.price * item_count(product,cart)
    
@register.filter(name = 'cart_price')
def cart_price(products, cart):
    sum = 0
    for p in products:
        sum+=total_price(p,cart)
    return sum


  