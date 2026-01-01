import time
from functools import wraps
from django.db import connection, reset_queries
from django.conf import settings

def db_debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not settings.DEBUG:
            return func(*args, **kwargs)

        reset_queries()
        start_time = time.time()

        result = func(*args, **kwargs)

        total_time = time.time() - start_time
        num_queries = len(connection.queries)

        print(f"\n📊 DB DEBUG — {func.__name__}")
        print(f"Queries: {num_queries}")
        print(f"Time: {total_time:.3f}s")

        for i, q in enumerate(connection.queries, start=1):
            print(f"\n{i}. ({q['time']}s)")
            print(q["sql"])

        return result
    return wrapper