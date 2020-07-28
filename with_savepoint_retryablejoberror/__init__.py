from functools import wraps
from odoo.addons.connector.exception import InvalidDataError, RetryableJobError

def with_savepoint_jobretryableerror(f):
    """
    Method decorator to automatically wrap method with a savepoint and raise a
    RetryableJobError on failure.

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
                raise RetryableJobError(str(e))
    return wrapper
