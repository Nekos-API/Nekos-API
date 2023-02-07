export default `
    # An ISO 8601 formatted datetime
    scalar Datetime

    enum Nsfw {
        sfw
        questionable
        nsfw
    }

    enum ImageOrientation {
        landscape
        portrait
        square
    }

    type _Source {
        name: String
        url: String
    }

    type _ImageDimens {
        height: Int
        width: Int
        aspectRatio: String
        orientation: ImageOrientation!
    }

    type _ImageMeta {
        eTag: String!
        size: Int!
        mimetype: String!
        color: String
        expires: Datetime!
        dimens: _ImageDimens!
    }

    type Artist {
        id: ID!
        name: String
        url: String
        images: Int
    }

    type Category {
        id: ID!
        name: String!
        description: String!
        nsfw: Boolean!
        type: String!
        images: Int
        createdAt: Datetime!
    }

    type Character {
        id: ID!
        name: String!
        description: String
        source: String
        createdAt: Datetime!
    }

    type Image {
        id: ID!
        url: String!
        artist: Artist
        source: _Source!
        original: Boolean
        nsfw: Nsfw
        categories: [Category!]
        characters: [Character!]
        createdAt: Datetime!
        meta: _ImageMeta!
    }

    type Query {
        getImage(id: ID!): Image!
        getRandomImages(limit: Int! = 1, categories: [String!]): [Image!]!
        getArtist(id: ID!): Artist!
        getArtists(limit: Int! = 10, offset: Int! = 0): [Artist!]!
        getArtistImages(id: ID!, limit: Int! = 10, offset: Int! = 0): [Image!]!
    }
`