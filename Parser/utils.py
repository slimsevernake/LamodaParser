import re
import json


def parse_sizes(sizes):
    splitted = re.findall("{[^}]*}", sizes)
    return [parse_size(parsed_size) for parsed_size in splitted]


def parse_size(size_data):
    result = json.loads(size_data)
    return result
