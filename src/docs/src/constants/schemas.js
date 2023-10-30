export const stringify = (json) => JSON.stringify(json, null, 4);

export const image_schema = {
    id: "integer",
    id_v2: "UUID?",
    image_url: "URL",
    sample_url: "URL",
    image_size: "integer",
    image_width: "integer",
    image_height: "integer",
    sample_size: "integer",
    sample_width: "integer",
    sample_height: "integer",
    source: "URL?",
    source_id: "integer?",
    rating: "string",
    verification: "verified",
    hash_md5: "string",
    hash_perceptual: "string",
    color_dominant: [
        "integer", "integer", "integer"
    ],
    color_palette: [
        [
            "integer", "integer", "integer"
        ]
    ],
    duration: "integer?",
    is_original: "boolean",
    is_screenshot: "boolean",
    is_flagged: "boolean",
    is_animated: "boolean",
    artist: "Artist?",
    character: "Character?",
    tags: [
        "Tag"
    ],
    created_at: "UNIX timestamp",
    updated_at: "UNIX timestamp",
};

export const tag_schema = {
    id: "integer",
    id_v2: "UUID?",
    name: "string",
    description: "string",
    is_nsfw: "boolean",
}

export const artist_schema = {
    id: "integer",
    id_v2: "UUID?",
    name: "string",
    aliases: [
        "string"
    ],
    image_url: "URL?",
    links: [
        "URL"
    ],
    policy_repost: "boolean",
    policy_credit: "boolean",
    policy_ai: "boolean",
};

export const character_schema = {
    id: "integer",
    id_v2: "UUID?",
    name: "string",
    aliases: [
        "string"
    ],
    description: "string",
    ages: [
        "integer"
    ],
    height: "integer?",
    weight: "integer?",
    gender: "string",
    species: "string",
    birthday: "string",
    nationality: "string",
    occupations: [
        "string"
    ],
    main_image_id: "integer?",
}

export const pagination = (items) => ({
    items: items,
    count: "integer",
});
