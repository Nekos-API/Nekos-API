import supabase from "../../utils/supabase/client";

import probe from "probe-image-size";
import parseImage from "./parsers";
import { prisma } from "@prisma/client";

export async function getImageJson(
    image,
    prismaClient,
    { expiry = 3600 } = { expiry: 3600 }
) {
    // Get the file object and image categories from the database
    var [file, categories, characters] = await prismaClient.$transaction([
        prismaClient.objects.findUnique({
            where: {
                id: image.file,
            },
        }),
        prismaClient.categories.findMany({
            where: {
                id: {
                    in: image.categories,
                },
            },
        }),
        prismaClient.characters.findMany({
            where: {
                id: {
                    in: image.characters,
                },
            },
        })
    ]);

    // Get the signed URL for the file
    const { data } = await supabase.storage
        .from("nekos-api")
        .createSignedUrl(file.name, expiry);

    // Get the artist for the image
    var artist = image.artist
        ? await prismaClient.artists.findUnique({
              where: {
                  id: image.artist,
              },
          })
        : null;

    if (image.height in [0, null] || image.width in [0, null]) {
        // If the image height or width is 0 or null, then the image dimensions need to be updated
        const { height, width } = await probe(data.signedUrl);

        image.height = height;
        image.width = width;

        // Not awaited because it is not necessary to wait for it to finish
        prismaClient.images
            .update({
                where: {
                    id: image.id,
                },
                data: {
                    height: height,
                    width: width,
                },
            })
            .then(() => {
                // Do nothing after the image dimensions are updated
            });
    }

    return await parseImage(
        image,
        file,
        data.signedUrl,
        artist,
        categories,
        characters,
        expiry
    );
}

export async function getManyImagesJson(
    images,
    prismaClient,
    { expiry = 3600 } = { expiry: 3600 }
) {
    var result = [];

    // Array with all the file ids so we can get the signed urls in a single call.
    var fileIds = [];

    images.map((item) => {
        fileIds.push(item.file);
    });

    // Get the files from the database
    var files = await prismaClient.objects.findMany({
        where: {
            id: {
                in: fileIds,
            },
        },
    });

    // Two different variables are used to store the file names and ids because the
    // order of the files returned by the database is not guaranteed to be the same as
    // the order of the file ids in the `fileIds` array.
    var fileNames = [];
    var filesById = {};

    files.map((file) => {
        fileNames.push(file.name);
        filesById[file.id] = file;
    });

    // Get the signed urls for the files
    const { data, error } = await supabase.storage
        .from("nekos-api")
        .createSignedUrls(fileNames, expiry);

    if (error) {
        throw error;
    }

    // Create a map of the signed urls so they can be accessed by the file name
    var signedUrls = {};

    data.map((file) => {
        let row = files.find((row) => {
            return (row.name = file.path);
        });
        signedUrls[row.name] = file.signedUrl;
    });

    // Array with all the artist ids so we can get the artists in a single call.
    var artistIds = [];

    images.map((image) => {
        // Add all artist ids to the array. Avoid duplicates to reduce the expensiveness of the db query.
        if (artistIds.indexOf(image.artist) == -1 && image.artist != null) {
            artistIds.push(image.artist);
        }
    });

    // Get all the artists
    var artists = await prismaClient.artists.findMany({
        where: {
            id: {
                in: artistIds,
            },
        },
    });

    // Create a map of the artists so they can be accessed by the artist id
    var artistMap = {};

    artists.map((artist) => {
        artistMap[artist.id] = artist;
    });

    // Get all the categories
    var categoryIds = [];

    images.map((image) => {
        image.categories.map((categoryId) => {
            // Add all category ids to the array. Avoid duplicates to reduce the expensiveness of the db query.
            if (categoryIds.indexOf(categoryId) == -1) {
                categoryIds.push(categoryId);
            }
        });
    });

    // Get all the categories
    var categories = await prismaClient.categories.findMany({
        where: {
            id: {
                in: categoryIds,
            },
        },
    });

    // Create a map of the categories so they can be accessed by the category id
    var categoryMap = {};

    categories.map((category) => {
        categoryMap[category.id] = category;
    });

    var characterIds = [];

    images.map((image) => {
        image.characters.map((characterId) => {
            // Add all character ids to the array. Avoid duplicates to reduce the expensiveness of the db query.
            if (characterIds.indexOf(characterId) == -1) {
                characterIds.push(characterId);
            }
        });
    });

    // Get all the characters
    var characters = await prismaClient.characters.findMany({
        where: {
            id: {
                in: characterIds,
            },
        },
    });

    // Create a map of the characters so they can be accessed by the character id
    var characterMap = {};

    characters.map((character) => {
        characterMap[character.id] = character;
    });

    // Add the images to the result array
    for (var image of images) {
        // Create an array with the categories for the image
        var imageCategories = [];

        image.categories.map((categoryId) => {
            // Get the category from the map
            let category = categoryMap[categoryId];

            // Add the category to the array that will be returned.
            imageCategories.push(category);
        });

        var imageCharacters = [];

        image.characters.map((characterId) => {
            // Get the character from the map
            let character = characterMap[characterId];

            // Add the character to the array that will be returned.
            imageCharacters.push(character);
        });

        // Create the artist var. This will be overriden if the image has an artist.
        let artist = null;

        if (image.artist) {
            artist = artistMap[image.artist];
        }

        // Get the file from the map
        const file = filesById[image.file];

        if (
            image.height in [0, null, undefined] ||
            image.width in [0, null, undefined]
        ) {
            // If the image dimensions are not set, get them from the image file.
            const { height, width } = await probe(signedUrls[file.name]);

            image.height = height;
            image.width = width;

            // Not awaited because it is not necessary to wait for it to finish
            prismaClient.images
                .update({
                    where: {
                        id: image.id,
                    },
                    data: {
                        height: height,
                        width: width,
                    },
                })
                .then(() => {
                    // Do nothing after they are updated. This will run in background.
                });
        }

        // Add the image to the result array
        result.push(
            await parseImage(
                image,
                file,
                signedUrls[file.name],
                artist,
                imageCategories,
                imageCharacters,
                expiry
            )
        );
    }

    return result;
}
