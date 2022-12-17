from django import template

register = template.Library()
@register.filter(name = 'currency')
def currency(number):
    return "$ "+str(number)

@register.filter(name = 'multiply')
def total_price(price, quantity):
    return price * quantity
  