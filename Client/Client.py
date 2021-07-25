# Field to test Master
import copy

from Master.Master import Master

master = Master()


products = master.parse_product_by_tag("портупея")

tester = copy.copy(products[0])

tester.price = 100
tester.sizes = [{'available': False, 'value': "123", 'brandSize': "40"}]

tempo = master.parse_product_by_sku(tester.article)

print(tempo)
print(products[0])

master.check_product_changed(tester, products[0])
#master.check_product_changed(tester, products[0])

