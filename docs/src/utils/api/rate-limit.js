import redis from "./redis";
import requestIp from "request-ip";
import NextCors from "nextjs-cors";
import { GraphQLError } from "graphql";

export default async function checkRateLimit(
    req,
    res = null,
    { 
        ttl = 1,            // Time in seconds to block an IP after being rate limited
        limit = 1,          // Amount of requests before being blocked for `ttl` seconds
        timeout_ttl = 3600, // Time in seconds to block an IP after being rate limited `timeout_limit` times
        timeout_limit = 10  // Amount of times an IP can be rate limited before being blocked for `timeout_ttl` seconds 
    } = {}
) {
    const ip = requestIp.getClientIp(req); // The client's IP
    const key = `ratelimit:${ip}`; // Key to store the current amount of requests of an IP during `ttl` seconds in redis
    const timeout_key = `${key}:timeout`; // Key to store the amount of times an IP was rate limited in `timeout_ttl` seconds

    var current = await redis.get(key);
    if (current === null) current = 0;
    var timeout = await redis.get(timeout_key);
    if (timeout === null) timeout = 0;

    await redis.set(key, current + 1, {
        ex: ttl,
        keepTtl: true
    });

    if (res) {
        await NextCors(req, res, {
            // Options
            methods: ["GET", "HEAD", "PUT", "PATCH", "POST", "DELETE"],
            origin: "*",
            optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
        });

        res.setHeader("X-RateLimit-Limit", limit);
        res.setHeader("X-RateLimit-Remaining", limit - (current + 1) > 0 ? limit - (current + 1) : 0);
        res.setHeader("X-RateLimit-Reset", await redis.ttl(key))
    }

    if (timeout >= timeout_limit) {
        // The IP has made more than `timeout_limit` requests in less than `timeout_ttl` seconds
        await redis.set(timeout_key, timeout + 1, {
            ex: timeout_ttl,
            keepTtl: true
        });
        if (res) {
            let retry_after = await redis.ttl(timeout_key)
            res.setHeader("Retry-After", retry_after);
            res.setHeader("X-RateLimit-Reset", retry_after);
            res.status(429).json({
                code: 429,
                message:
                    "You have exceeded the rate limit too many times. Please try again later.",
                success: false,
            });
        } else {
            throw new GraphQLError(
                "You have exceeded the rate limit too many times. Please try again later."
            );
        }
        return false;
    } else if (current >= limit) {
        // The IP has made more requests than `limit` in less than `ttl` seconds
        await redis.set(timeout_key, timeout + 1, {
            ex: ttl,
            keepTtl: true
        });
        if (res) {
            let retry_after = await redis.ttl(key)
            res.setHeader("Retry-After", retry_after);
            res.setHeader("X-RateLimit-Reset", retry_after);
            res.status(429).json({
                code: 429,
                message:
                    "You have exceeded the rate limit. Please try again later.",
                success: false,
            });
        } else {
            throw new GraphQLError(
                "You have exceeded the rate limit. Please try again later."
            );
        }
        return false;
    }

    return true;
}
