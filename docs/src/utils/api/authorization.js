import { PrismaClient } from "@prisma/client";

export async function getScopesFromToken(req, res, required = false) {
    const { authorization: token } = req.headers;

    if (!token && required) {
        res.status(401).json({
            code: 401,
            message: "You need an access token to access this resource.",
            success: false
        })
        return false;
    } else if (!token && !required) {
        return [];
    }

    const exp = /^Bearer (?<token>[0-9a-zA-Z]{100})$/
    
    if (!exp.test(token)) {
        res.status(401).json({
            code: 401,
            message: "The authentication token is invalid. It should match `^Bearer [0-9a-zA-Z]{100}$`.",
            success: false
        })
        return false;
    }

    const prisma = new PrismaClient();

    const row = await prisma.tokens.findUnique({
        where: {
            token: exp.exec(token).groups.token
        }
    })

    if (!row) {
        res.status(401).json({
            code: 401,
            message: "The authentication token is invalid.",
            success: false
        })
        return false;
    }

    prisma.$disconnect();

    return row.scopes;
}


export function checkExpiryPermissions(res, expiry, scopes) {
    if (expiry !== "3600") {
        if (scopes.length === 0) {
            res.status(401).json({
                code: 401,
                message:
                    "You need to be authorized to set a custom expire time for image links.",
                success: false,
            });
            return false;
        } else {
            const expiry_scopes = scopes.map((scope, index) => {
                if (/^image:custom-expiry(:[0-9]+)?$/.test(scope)) {
                    return scope;
                }
            });
            if (expiry_scopes.length === 0) {
                res.status(403).json({
                    code: 403,
                    message:
                        "Your access token does not have permission to set a custom expiry time for image links.",
                    success: true,
                });
                return false;
            }
            if (!/^[0-9]+$/.test(expiry) || parseInt(expiry) <= 30) {
                res.status(400).json({
                    code: 400,
                    message:
                        "The expiry parameter must represent a time in seconds equal or greater than 30.",
                    success: false,
                });
                return false;
            }

            const scope = expiry_scopes[0]
            const max_expiry_time = scope.split(":").length == 3 ? parseInt(scope.split(":")[2]) : null
            
            expiry = parseInt(expiry)

            if (max_expiry_time !== null && expiry > max_expiry_time) {
                res.status(403).json({
                    code: 403,
                    message: `You are not permitted to set an expiry time greater than ${max_expiry_time} seconds.`,
                    success: false
                })
                return false;
            }
        }
    }

    return true;
}