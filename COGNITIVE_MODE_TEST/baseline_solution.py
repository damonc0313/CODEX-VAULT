"""
BASELINE SOLUTION - No cognitive modes active
Just default pattern matching from training.

Problem: Rate limiter for API
"""

import time
from collections import defaultdict
from typing import Dict

class RateLimiter:
    """Simple rate limiter using token bucket."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def allow_request(self, user_id: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        
        # Clean old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check limit
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        
        return False

# Usage
limiter = RateLimiter(max_requests=10, window_seconds=60)

# Test
user = "user123"
for i in range(12):
    allowed = limiter.allow_request(user)
    print(f"Request {i+1}: {'Allowed' if allowed else 'Blocked'}")
