import { PrismaClient } from "@prisma/client";
import { GraphQLError } from 'graphql'
import { getManyImagesJson } from "../../../db";

export default async function getArtistImages(_, args, context) {
    const { id, limit = 10, offset = 0 } = args;

    if (!/^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$/gi.test(id)) {
        throw GraphQLError("Provided ID is not a valid UUID v4.")
    }

    if (limit <= 0 || limit > 25) {
        throw new GraphQLError("Invalid value for `limit` parameter. Expected a number between 1 and 25.")
    }

    if (offset < 0) {
        throw new GraphQLError("Invalid value for `offset` parameter. Expected a number greater or equal to 0.")
    }

    const prisma = new PrismaClient();

    const images = await prisma.images.findMany({
        where: {
            artist: id
        },
        take: limit,
        skip: offset
    })

    if (images.length == 0) {
        throw GraphQLError(`Could not find artist with ID \`${id}\`.`)
    }

    const images_json = await getManyImagesJson(images, prisma)

    prisma.$disconnect()

    return images_json
}