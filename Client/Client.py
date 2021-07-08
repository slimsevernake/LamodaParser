# Field to test Master
import copy

from Master.Master import Master

master = Master()


data = master.parse_product_by_tag("портупея")
el = copy.copy(data[0])

el.price = 1
master.is_product_changed(el)
