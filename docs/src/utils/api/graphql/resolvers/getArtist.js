import { PrismaClient } from "@prisma/client";
import { parseArtist } from "../../../db/parsers";
import { GraphQLError } from 'graphql'

export default async function getArtist(_, args, context) {
    const { id } = args;

    if (!/^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$/gi.test(id)) {
        throw GraphQLError("Provided ID is not a valid UUID v4.")
    }

    const prisma = new PrismaClient();

    const artist = await prisma.artists.findUnique({
        where: {
            id
        }
    })

    if (!artist) {
        throw GraphQLError(`Could not find artist with ID \`${id}\`.`)
    }

    const artist_json = await parseArtist(artist, prisma)

    prisma.$disconnect()

    return artist_json
}