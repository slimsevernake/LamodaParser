# Field to test Master
from Master.Master import Master

master = Master()


data = master.parse_product_by_tag("nike")

print(data)