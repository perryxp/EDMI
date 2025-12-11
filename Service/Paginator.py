import math

class Paginator:
    @staticmethod
    def paginate(items, count, page = 1, limit = 20):
        return {
            'pagination': {
                'page': page,
                'limit': limit,
                'total': count,
                'total_pages': math.ceil(count / limit),
            },
            'data': items
        }
