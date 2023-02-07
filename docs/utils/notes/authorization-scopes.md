# Authorization scopes

- `api:ratelimit:disabled`: Disables rate limiting.
- `api:ratelimit:{requests}-{window_secs}-{timeout_after}`: Changes rate limit to allow `requests` requests in the same `window_secs` seconds, being blocked for 1 hour after getting rate limited `timeout_after` times.
- `image:list`: Access to a paginated list of all images at `/api/image`
- `image:custom-expiry`: Access to custom image links expiry times (*Partially implemented*)
- `image:custom-expiry:{max_secs}`: Access to custom image links expiry times of up to `max_secs` seconds