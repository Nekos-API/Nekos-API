require("dotenv").config();

const { PrismaClient } = require("@prisma/client");
const { createClient } = require("@supabase/supabase-js");
const { getColorFromURL } = require("color-thief-node");

const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_ANON_SUPABASE_KEY
);

const prisma = new PrismaClient();

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

async function main() {
    const images = await prisma.images.findMany({
        where: {
            color: null,
        }
    });

    const objects = await prisma.objects.findMany({
        where: {
            id: {
                in: images.map((img) => img.file)
            }
        }
    });

    console.log(`Found ${objects.length} objects to update.`)

    var i = 1;

    for (const object of objects) {
        const signedUrl = (
            await supabase.storage
                .from("nekos-api")
                .createSignedUrl(object.name, 60)
        ).data.signedUrl;

        const color = await getColorFromURL(signedUrl);

        await prisma.images.update({
            where: {
                file: object.id,
            },
            data: {
                color: {
                    set: rgbToHex(color[0], color[1], color[2])
                },
            },
        });

        console.log(`Updated ${object.id} - ${rgbToHex(color[0], color[1], color[2])} - (${i++}/${objects.length})`)
    }
}

main();