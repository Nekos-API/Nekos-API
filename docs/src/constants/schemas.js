export const stringify = (json) => JSON.stringify(json, null, 4);

export const image_ref = {
    type: "image",
    id: "UUID",
};

export const gif_ref = {
    type: "gif",
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

export const list_ref = {
    type: "list",
    id: "String",
};

export const reaction_ref = {
    type: "reaction",
    id: "UUID",
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
            isActive: "Boolean",
            isStaff: "Boolean",
            isSuperuser: "Boolean",
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
                self: "https://api.nekosapi.com/v2/users/:id/relationships/following",
                related: "https://api.nekosapi.com/v2/users/:id/following",
            },
        },
        followers: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/followers",
                related: "https://api.nekosapi.com/v2/users/:id/followers",
            },
        },
        followedArtists: {
            meta: {
                count: "Integer",
            },
            data: [artist_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/followed-artists",
                related:
                    "https://api.nekosapi.com/v2/users/:id/followed-artists",
            },
        },
        followedCharacters: {
            meta: {
                count: "Integer",
            },
            data: [character_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/followed-characters",
                related:
                    "https://api.nekosapi.com/v2/users/:id/followed-characters",
            },
        },
        followedCategories: {
            meta: {
                count: "Integer",
            },
            data: [category_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/followed-categories",
                related:
                    "https://api.nekosapi.com/v2/users/:id/followed-categories",
            },
        },
        likedImages: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/liked-images",
                related: "https://api.nekosapi.com/v2/users/:id/liked-images",
            },
        },
    },
    meta: {
        user: {
            isFollowing: "Boolean?",
            isBeingFollowed: "Boolean?",
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/users/:id",
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
            isActive: "Boolean",
            isStaff: "Boolean",
            isSuperuser: "Boolean",
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
                self: "https://api.nekosapi.com/v2/users/:id/relationships/following",
                related: "https://api.nekosapi.com/v2/users/:id/following",
            },
        },
        followers: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/followers",
                related: "https://api.nekosapi.com/v2/users/:id/followers",
            },
        },
        followedArtists: {
            meta: {
                count: "Integer",
            },
            data: [artist_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/followed-artists",
                related:
                    "https://api.nekosapi.com/v2/users/:id/followed-artists",
            },
        },
        followedCharacters: {
            meta: {
                count: "Integer",
            },
            data: [character_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/followed-characters",
                related:
                    "https://api.nekosapi.com/v2/users/:id/followed-characters",
            },
        },
        followedCategories: {
            meta: {
                count: "Integer",
            },
            data: [category_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/followed-categories",
                related:
                    "https://api.nekosapi.com/v2/users/:id/followed-categories",
            },
        },
        likedImages: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/liked-images",
                related: "https://api.nekosapi.com/v2/users/:id/liked-images",
            },
        },
        savedImages: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/saved-images",
                related: "https://api.nekosapi.com/v2/users/:id/saved-images",
            },
        },
        discord: {
            links: {
                self: "https://api.nekosapi.com/v2/users/:id/relationships/discord",
                related: "https://api.nekosapi.com/v2/users/:id/discord",
            },
            data: discord_ref,
        },
    },
    meta: {
        user: {
            isFollowing: "Boolean?",
            isBeingFollowed: "Boolean?",
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/users/:id",
    },
};

export const image_schema = {
    type: "image",
    id: "UUID",
    attributes: {
        file: "URL",
        title: "String",
        colors: {
            dominant: "String?",
            palette: ["String?"],
        },
        source: {
            name: "String?",
            url: "URL?",
        },
        dimens: {
            height: "Integer?",
            width: "Integer?",
            aspectRatio: "String?",
            orientation: "String?",
        },
        isOriginal: "Boolean",
        verificationStatus: "String",
        ageRating: "String?",
        metadata: {
            mimetype: "String?",
            fileSize: "Integer?",
        },
        timestamps: {
            created: "ISO 8601",
            updated: "ISO 8601",
        },
    },
    relationships: {
        uploader: {
            links: {
                self: "https://api.nekosapi.com/v2/images/:id/relationships/uploader",
                related: "https://api.nekosapi.com/v2/images/:id/uploader",
            },
            data: user_ref,
        },
        artist: {
            links: {
                self: "https://api.nekosapi.com/v2/images/:id/relationships/artist",
                related: "https://api.nekosapi.com/v2/images/:id/artist",
            },
            data: artist_ref,
        },
        categories: {
            meta: {
                count: "Integer",
            },
            data: [category_ref],
            links: {
                self: "https://api.nekosapi.com/v2/images/:id/relationships/categories",
                related: "https://api.nekosapi.com/v2/images/:id/categories",
            },
        },
        characters: {
            meta: {
                count: "Integer",
            },
            data: [character_ref],
            links: {
                self: "https://api.nekosapi.com/v2/images/:id/relationships/characters",
                related: "https://api.nekosapi.com/v2/images/:id/characters",
            },
        },
        likedBy: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/images/:id/relationships/liked-by",
                related: "https://api.nekosapi.com/v2/images/:id/liked-by",
            },
        },
    },
    meta: {
        user: {
            liked: "Boolean?",
            saved: "Boolean?",
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/images/:id",
    },
};

export const artist_schema = {
    type: "artist",
    id: "UUID",
    attributes: {
        name: "String",
        aliases: ["String"],
        imageUrl: "URL?",
        officialLinks: ["URL"],
        timestamps: {
            created: "ISO 8601",
            updated: "ISO 8601",
        },
    },
    relationships: {
        images: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/artists/:id/relationships/images",
                related: "https://api.nekosapi.com/v2/artists/:id/images",
            },
        },
        followers: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/artists/:id/relationships/followers",
                related: "https://api.nekosapi.com/v2/artists/:id/followers",
            },
        },
    },
    meta: {
        user: {
            isFollowing: "Boolean?",
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/artists/:id",
    },
};

export const character_schema = {
    type: "character",
    id: "UUID",
    attributes: {
        name: {
            first: "String?",
            last: "String?",
            aliases: ["String"],
        },
        description: "String?",
        gender: "String?",
        species: "String?",
        ages: ["Integer"],
        birthDate: "String?",
        nationality: "String?",
        occupations: ["String"],
        timestamps: {
            created: "ISO 8601",
            updated: "ISO 8601",
        },
    },
    relationships: {
        images: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/characters/:id/relationships/images",
                related: "https://api.nekosapi.com/v2/characters/:id/images",
            },
        },
        followers: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/characters/:id/relationships/followers",
                related: "https://api.nekosapi.com/v2/characters/:id/followers",
            },
        },
    },
    meta: {
        user: {
            isFollowing: "Boolean?",
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/characters/:id",
    },
};

export const category_schema = {
    type: "category",
    id: "UUID",
    attributes: {
        name: "String",
        description: "String",
        sub: "String",
        isNsfw: "Boolean",
        timestamps: {
            created: "ISO 8601",
            updated: "ISO 8601",
        },
    },
    relationships: {
        images: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/categories/:id/relationships/images",
                related: "https://api.nekosapi.com/v2/categories/:id/images",
            },
        },
        followers: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/categories/:id/relationships/followers",
                related: "https://api.nekosapi.com/v2/categories/:id/followers",
            },
        },
    },
    meta: {
        user: {
            isFollowing: "Boolean?",
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/categories/:id",
    },
};

export const list_schema = {
    type: "list",
    id: "UUID",
    attributes: {
        name: "String",
        description: "String?",
        isPrivate: "Boolean",
        timestamps: {
            created: "ISO 8601",
            updated: "ISO 8601",
        },
    },
    relationships: {
        user: {
            links: {
                self: "https://api.nekosapi.com/v2/lists/:id/relationships/user",
                related: "https://api.nekosapi.com/v2/lists/:id/user",
            },
            data: user_ref,
        },
        images: {
            meta: {
                count: "Integer",
            },
            data: [image_ref],
            links: {
                self: "https://api.nekosapi.com/v2/lists/:id/relationships/images",
                related: "https://api.nekosapi.com/v2/lists/:id/images",
            },
        },
        followers: {
            meta: {
                count: "Integer",
            },
            data: [user_ref],
            links: {
                self: "https://api.nekosapi.com/v2/lists/:id/relationships/followers",
                related: "https://api.nekosapi.com/v2/lists/:id/followers",
            },
        },
    },
    meta: {
        user: {
            isFollowing: "Boolean?",
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/lists/:id",
    },
};

export const gif_schema = {
    type: "gif",
    id: "UUID",
    attributes: {
        files: {
            original: {
                url: "URL",
                dimens: {
                    width: "Integer?",
                    height: "Integer?",
                    aspectRatio: "String?",
                    orientation: "String?",
                },
                metadata: {
                    mimetype: "String?",
                    size: "Integer?",
                    frames: "Integer?",
                    duration: "String?",
                },
            },
            consistent: {
                url: "URL",
                dimens: {
                    width: "Integer?",
                    height: "Integer",
                    aspectRatio: "16:9",
                    orientation: "landscape",
                },
                metadata: {
                    mimetype: "String",
                    size: "Integer?",
                    frames: "Integer?",
                    duration: "String?",
                },
            },
        },
        text: "String?",
        colors: {
            dominant: "String?",
            palette: ["String"],
        },
        source: {
            name: "String?",
            url: "URL?",
        },
        verificationStatus: "String?",
        ageRating: "String",
        isSpoiler: "Boolean",
        emotions: ["String"],
        timestamps: {
            created: "ISO 8601",
            updated: "ISO 8601",
        },
    },
    relationships: {
        reactions: {
            meta: {
                count: "Integer?",
            },
            data: [reaction_ref],
            links: {
                self: "https://api.nekosapi.com/v2/gifs/:id/relationships/reactions",
                related: "https://api.nekosapi.com/v2/gifs/:id/reactions",
            },
        },
        characters: {
            meta: {
                count: "Integer",
            },
            data: [character_ref],
            links: {
                self: "https://api.nekosapi.com/v2/gifs/:id/relationships/characters",
                related: "https://api.nekosapi.com/v2/gifs/:id/characters",
            },
        },
        categories: {
            meta: {
                count: "Integer",
            },
            data: [category_ref],
            links: {
                self: "https://api.nekosapi.com/v2/gifs/:id/relationships/categories",
                related: "https://api.nekosapi.com/v2/gifs/:id/categories",
            },
        },
        uploader: {
            links: {
                self: "https://api.nekosapi.com/v2/gifs/:id/relationships/uploader",
                related: "https://api.nekosapi.com/v2/gifs/:id/uploader",
            },
            data: user_ref,
        },
    },
    links: {
        self: "https://api.nekosapi.com/v2/gifs/:id",
    },
};

export const reaction_schema = {
    type: "reaction",
    id: "UUID",
    attributes: {
        name: "String",
        isNsfw: "Boolean",
    },
};

export const pagination = (items, included) => ({
    links: {
        first: "URL",
        last: "URL",
        next: "URL?",
        prev: "URL?",
    },
    data: items,
    included,
    meta: {
        pagination: {
            count: "Integer",
            limit: "Integer",
            offset: "Integer",
        },
    },
});

export const resource = (data, included) => ({ data, included });
