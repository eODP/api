from config import Config


def paginate(query_object, page):
    per_page = Config.PER_PAGE
    return query_object.paginate(page, per_page, False).items
