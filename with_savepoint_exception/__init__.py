from functools import wraps

def with_savepoint_exception(f):
    """
    Method decorator to automatically wrap method with a savepoint and raise a
    generic Exception on failure rather than re-raise the original exception.

    We need to wrap some actions with a savepoint in order to deal with job
    queue preventing the stock.quant _update_reserved_quantity exceptions not
    rolling back all actions, resulting in a stock.move being confirmed, but
    inventory being done.
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        with self.env.cr.savepoint():
            try:
                return f(self, *args, **kwargs)
            except Exception as e:
                raise Exception(str(e))
    return wrapper
