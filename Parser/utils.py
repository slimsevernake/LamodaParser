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


def generate_name_from_pattern(pattern: str):
    return " ".join(re.findall("\+\S*", pattern))


def get_forbidden(pattern: str):
    temp = pattern.lower()
    forbidden = re.findall("\-\S*", temp)
    return list(map(lambda x: x.replace("-", ""), forbidden))


def get_required(pattern: str):
    temp = pattern.lower()
    required = re.findall("\+\S*", temp)
    return list(map(lambda x: x.replace("+", ""), required))


def check_name(tag: str, pattern: str):
    temp_tag = tag.lower().replace(" ", "")
    forbidden = get_forbidden(pattern)
    required = get_required(pattern)
    for forbidden_piece in forbidden:
        if forbidden_piece in temp_tag:
            return False
    for required_piece in required:
        if required_piece not in temp_tag:
            return False
    return True


def get_sku_from_url(url: str):
    return get_proper_sku(url.split("/")[2])


def get_proper_sku(sku):
    return sku.upper()
