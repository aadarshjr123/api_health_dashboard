import time
import logging


def retry(max_retries=3, delay=2, backoff=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.warning(f"Attempt {attempts}/{max_retries} failed: {e}")
                    if attempts == max_retries:
                        logging.error(f"Max retries reached for {func.__name__}")
                        raise
                    sleep_time = delay * (backoff ** (attempts - 1))
                    time.sleep(sleep_time)

        return wrapper

    return decorator
