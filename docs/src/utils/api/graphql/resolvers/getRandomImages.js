import { Prisma, PrismaClient } from "@prisma/client";
import { getManyImagesJson } from "../../../db";
import { GraphQLError } from 'graphql'

export default async function getRandomImages(_, args, context) {
    const { limit = 1, categories = [] } = args;

    if (limit <= 0 || limit > 25) {
        throw new GraphQLError("Invalid value for `limit` parameter. Expected a number between 1 and 25.")
    }

    const prisma = new PrismaClient();

    const bernoulliPercentage = 20;

    var images;

    if (categories.length == 0) {
        images = await prisma.$queryRaw`SELECT * FROM "Images" TABLESAMPLE BERNOULLI (${bernoulliPercentage}) ORDER BY RANDOM() LIMIT (${parseInt(limit)})`;
    } else {
        const matchingCategories = await prisma.$queryRaw`SELECT * FROM "Categories" WHERE name ILIKE ANY(ARRAY[${Prisma.join(categories)}])`
        if (categories.length != Array.from(matchingCategories).length) {
            var nonMatchingCategories = categories.filter(category => !matchingCategories.map(category => category.name.toLowerCase()).includes(category))
            
            throw new GraphQLError(`Invalid value for \`categories\` parameter. The following categories do not exist: ${nonMatchingCategories.join(", ")}`)
        }
        images = await prisma.$queryRaw`SELECT * FROM "Images" TABLESAMPLE BERNOULLI (${bernoulliPercentage}) WHERE categories @> ARRAY(SELECT id FROM "Categories" WHERE name ILIKE ANY(ARRAY[${Prisma.join(categories)}])) ORDER BY RANDOM() LIMIT (${parseInt(limit)})`;
    }

    prisma.$disconnect()

    if (images.length == 0) {
        throw new GraphQLError("Could not find images with the selected categories. If you believe that this category has got images, you should repeat the request up to 2 times more.")
    }

    return await getManyImagesJson(images, prisma)
}