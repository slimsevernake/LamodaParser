import re
import json


def parse_sizes(sizes):
    splitted = re.findall("{[^}]*}", sizes)
    result_wo_filter = [parse_size(parsed_size) for parsed_size in splitted]
    return list(filter(lambda x: x is not None, result_wo_filter))


def parse_size(size_data):
    result = json.loads(size_data)
    if result["available"]:
        return result
    else:
        return None
