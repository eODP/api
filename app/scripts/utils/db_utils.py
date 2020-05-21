import re


def allowed_params(attributes_list, params):
    def format_value(value):
        if isinstance(value, str) and re.search(r"^ *$", value):
            return None
        else:
            return value

    return {k: format_value(v) for (k, v) in params.items() if k in attributes_list}


def trim_doc_string(string):
    """
    Remove newline, begining and end spaces, multiple concurrent spaces
    from a doc string
    """
    return re.sub(" +", " ", string.replace("\n", " ").strip())


def add_null_queries(sql, attributes):
    """
    Looks for attributes whose value is None, and changes the sql string from
    field = value to field is NULL.
    """
    for k, v in attributes.items():
        if v is None and k in sql:
            # NOTE: regex replaces " <text> = :<key>" with " <text> IS NULL"
            sql = re.sub(rf" ([\w._]+) *= *:{k}( |;)", r" \1 IS NULL\2", sql)

    return sql
