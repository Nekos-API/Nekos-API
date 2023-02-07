import checkRateLimit from "./rate-limit";
import { getScopesFromToken } from "./authorization";

// Returns the authentication token's scopes if any, otherwise returns an empty
// array. If the response was set by the middleware (this function) returns
// false and the connection should be closed.
export async function middleware(
    req,
    res,
    { authorization: { required } } = {
        authorization: {
            required: false,
        },
    }
) {
    const scopes = await getScopesFromToken(req, res, required);

    if (scopes === false) {
        return false;
    }

    var ratelimit_requests = 1;
    var ratelimit_ttl = 1;
    var ratelimit_timeout_limit = 10;

    const rate_limit_scope = scopes.filter((value, index) => {
        const exp = /^api:ratelimit:[0-9]+-[0-9]+-[0-9]+/;
        return exp.test(value);
    })[0];

    if (rate_limit_scope !== undefined) {
        const options = rate_limit_scope
            .split(":")[2]
            .split("-")
            .map((value, index) => {
                return parseInt(value);
            });
        ratelimit_requests = options[0];
        ratelimit_ttl = options[1];
        ratelimit_timeout_limit = options[2];
    }

    if (
        scopes
            .map((scope) => scope.toLowerCase())
            .includes("api:ratelimit:disabled")
    ) {
        return scopes;
    } else {
        if (
            !(await checkRateLimit(req, res, {
                ttl: ratelimit_ttl,
                limit: ratelimit_requests,
                timeout_limit: ratelimit_timeout_limit,
            }))
        ) {
            return false;
        } else {
            return scopes;
        }
    }
}
