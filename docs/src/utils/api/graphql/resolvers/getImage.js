import { PrismaClient } from "@prisma/client";
import { getImageJson } from "../../../db";
import { GraphQLError } from 'graphql'

export default async function getImage(_, args, context) {
    const { id } = args;

    if (!/^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$/gi.test(id)) {
        throw GraphQLError("Provided ID is not a valid UUID v4.")
    }

    const prisma = new PrismaClient();

    const image = await prisma.images.findUnique({
        where: {
            id
        }
    })

    if (!image) {
        throw GraphQLError(`Could not find image with ID \`${id}\`.`)
    }

    const image_json = await getImageJson(image, prisma)

    prisma.$disconnect()

    return image_json
}