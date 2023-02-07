import { PrismaClient } from "@prisma/client";
import { parseArtists } from "../../../db/parsers";
import { GraphQLError } from "graphql";

export default async function getArtist(_, args, context) {
    const { limit = 10, offset = 0 } = args;

    if (limit <= 0 || limit > 25) {
        throw new GraphQLError(
            "Invalid value for `limit` parameter. Expected a number between 1 and 25."
        );
    }

    if (offset < 0) {
        throw new GraphQLError(
            "Invalid value for `offset` parameter. Expected a number greater or equal to 0."
        );
    }

    const prisma = new PrismaClient();

    const artists = await prisma.artists.findMany({
        take: limit,
        skip: offset,
    });

    prisma.$disconnect();

    const artists_json = await parseArtists(artists);

    return artists_json;
}
