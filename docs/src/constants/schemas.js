export function stringify(json) {
    return JSON.stringify(json, null, 4);
}

export const image_ref = {
    type: "image",
    id: "UUID",
};

export const artist_ref = {
    type: "artist",
    id: "UUID",
};

export const category_ref = {
    type: "category",
    id: "UUID",
};

export const character_ref = {
    type: "character",
    id: "UUID",
};

export const user_ref = {
    type: "user",
    id: "UUID",
};

export const discord_ref = {
    type: "discord-user",
    id: "String",
};

export const user_public_schema = {
    type: "user",
    id: "UUID",
    attributes: {
        username: "String",
        nickname: "String?",
        biography: "String?",
        avatarImage: "URL?",
        permissions: {
            isActive: "Bool",
            isStaff: "Bool",
            isSuperuser: "Bool",
        },
        timestamps: {
            joined: "ISO 8601",
        },
    },
    relationships: {
        following: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/following",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/following",
            },
        },
        followers: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/followers",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/followers",
            },
        },
        followedArtists: {
            meta: {
                count: "Integer",
            },
            data: [artist_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/followed-artists",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/followed-artists",
            },
        },
        followedCharacters: {
            meta: {
                count: "Integer",
            },
            data: [character_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/followed-characters",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/followed-characters",
            },
        },
        followedCategories: {
            meta: {
                count: "Integer",
            },
            data: [category_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/followed-categories",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/followed-categories",
            },
        },
        likedImages: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/liked-images",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/liked-images",
            },
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/users/<uuid:pk>",
    },
};

export const user_private_schema = {
    type: "user",
    id: "UUID",
    attributes: {
        username: "String",
        name: {
            first: "String?",
            last: "String?",
        },
        nickname: "String?",
        biography: "String?",
        avatarImage: "URL?",
        email: "String",
        secretKey: "String",
        permissions: {
            isActive: "Bool",
            isStaff: "Bool",
            isSuperuser: "Bool",
        },
        timestamps: {
            joined: "ISO 8601",
        },
    },
    relationships: {
        following: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/following",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/following",
            },
        },
        followers: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/followers",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/followers",
            },
        },
        followedArtists: {
            meta: {
                count: "Integer",
            },
            data: [artist_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/followed-artists",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/followed-artists",
            },
        },
        followedCharacters: {
            meta: {
                count: "Integer",
            },
            data: [character_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/followed-characters",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/followed-characters",
            },
        },
        followedCategories: {
            meta: {
                count: "Integer",
            },
            data: [category_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/followed-categories",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/followed-categories",
            },
        },
        likedImages: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/liked-images",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/liked-images",
            },
        },
        savedImages: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/saved-images",
                related:
                    "https://api.nekosapi.com/v2/users/<uuid:pk>/saved-images",
            },
        },
        discord: {
            links: {
                self: "https://api.nekosapi.com/v2/users/<uuid:pk>/relationships/discord",
                related: "https://api.nekosapi.com/v2/users/<uuid:pk>/discord",
            },
            data: discord_ref,
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/users/<uuid:pk>",
    },
};

export const pagination = (items, included = []) => {
    return {
        links: {
            first: "URL",
            last: "URL",
            next: "URL?",
            prev: "URL?",
        },
        data: items,
        included: included,
        meta: {
            pagination: {
                count: "Integer",
                limit: "Integer",
                offset: "Integer",
            },
        },
    };
};

export const resource = (data) => {
    return {
        data: data
    }
}
