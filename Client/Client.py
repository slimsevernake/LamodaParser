# Field to test Master
from Master.Master import Master

master = Master()


data = master.parse_product_by_tag("портупея")

el = data[0]

master.is_product_changed(el)
