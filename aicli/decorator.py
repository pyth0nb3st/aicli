import cProfile
import io
import pstats
from functools import wraps


def profile(func):
    @wraps(func)
    def wrapper(*args, kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, kwargs)
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
        ps.print_stats()
        print("性能分析结果:")
        print(s.getvalue())
        return result

    return wrapper
