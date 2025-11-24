# app/utils/circuit_breaker.py
import time
from functools import wraps
from app.metrics import circuit_breaker_state


class CircuitBreaker:
    """
    Simple Circuit Breaker pattern to protect failing services.
    States:
      🟢 CLOSED – normal operation
      🟠 OPEN – too many failures, block further calls
      🟡 HALF-OPEN – allow one test call after timeout
    """

    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
        circuit_breaker_state.set(0)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Reject if circuit is OPEN
            if self.state == "OPEN":
                circuit_breaker_state.set(1)
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                    circuit_breaker_state.set(2)
                else:
                    raise Exception("⚡ Circuit Breaker OPEN – skipping call")

            try:
                result = func(*args, **kwargs)
                if self.state in ["OPEN", "HALF_OPEN"]:
                    self.reset()
                circuit_breaker_state.set(0)
                return result

            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    circuit_breaker_state.set(1)
                raise e

        return wrapper

    def reset(self):
        """Return to normal (CLOSED) state."""
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_failure_time = None
        circuit_breaker_state.set(0)
