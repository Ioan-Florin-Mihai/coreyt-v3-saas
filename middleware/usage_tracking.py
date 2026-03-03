from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
import time


class UsageTrackingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        response: Response = await call_next(request)

        latency_ms = int((time.time() - start_time) * 1000)

        # Skip if not authenticated
        if not hasattr(request.state, "api_key_id"):
            return response

        # Store latency in state (for future logging)
        request.state.latency_ms = latency_ms

        return response