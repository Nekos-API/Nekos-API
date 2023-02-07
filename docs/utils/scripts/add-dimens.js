require("dotenv").config();

const { PrismaClient } = require("@prisma/client");
const { createClient } = require("@supabase/supabase-js");
const probe = require("probe-image-size");

const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_ANON_SUPABASE_KEY
);

const prisma = new PrismaClient();

function gcd(a, b) {
    if (b == 0) {
        return a;
    }
    return gcd(b, a % b);
}

function getAspectRatio(h, w) {
    var r = gcd(h, w);
    return `${w / r}:${h / r}`;
}

async function main() {
    const images = await prisma.images.findMany({
        where: {
            OR: {
                width: 0,
                height: 0,
            },
        },
    });

    const objects = await prisma.objects.findMany({
        where: {
            id: {
                in: images.map((img) => img.file),
            },
        },
    });

    var i = 1;

    for (const object of objects) {
        const signedUrl = (
            await supabase.storage
                .from("nekos-api")
                .createSignedUrl(object.name, 60)
        ).data.signedUrl;

        const dimensions = await probe(signedUrl);
        const aspect = getAspectRatio(dimensions.height, dimensions.width)

        await prisma.images.update({
            where: {
                file: object.id,
            },
            data: {
                width: dimensions.width,
                height: dimensions.height,
                aspect_ratio: aspect
            },
        });

        console.log(
            `Updated ${object.id} - ${dimensions.width}x${
                dimensions.height
            } ${aspect} - (${i++}/${objects.length})`
        );
    }

    console.log(`Updated ${objects.length} images`);
}

main();
