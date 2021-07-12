# Field to test Master
import copy

from Master.Master import Master

master = Master()


products = master.parse_product_by_tag("портупея")


tester = copy.copy(products[0])

tester.price = 100

master.check_product_changed(products[0], tester)

