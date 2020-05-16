import re


def allowed_params(attributes_list, params):
    def format_value(value):
        if isinstance(value, str) and re.search(r"^ *$", value):
            return None
        else:
            return value

    return {k: format_value(v) for (k, v) in params.items() if k in attributes_list}


def trim_doc_string(string):
    return re.sub(" +", " ", string.replace("\n", " ").strip())
