require('dotenv').config()

const { PrismaClient } = require('@prisma/client');
const probe = require('probe-image-size');
const prompt = require('prompt-sync')();
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_ANON_SUPABASE_KEY);

const prisma = new PrismaClient();


const FgBlue = "\x1b[34m"
const Reset = "\x1b[0m"

function highlight(msg) {
    return `${FgBlue}${msg}${Reset}`
}

async function inputSelect(name, values, many = false) {
    // The `values` param is either an array of strings or an array of objects with a `label` and a `value` property
    var value = null;

    if (values.length == 0) {
        console.log(`${name}: No values to select from`);
        return null;
    }

    var valuesMap = {};
    var validInputs = values.map((val) => {
        if (typeof val == "string") {
            valuesMap[val] = val;
            return val;
        } else {
            valuesMap[val.label] = val.value;
            return val.label;
        }
    });

    while (!validInputs.includes(value)) {
        value = prompt(`${name} (${validInputs.join("/")}): `);

        if (many) {
            value = value.split(",");
        }

        if (!many && !validInputs.includes(value)) {
            console.log(`Invalid input, please try again`);
        } else if (many) {
            var invalid = value.filter((val) => !validInputs.includes(val));

            if (invalid.length > 0) {
                console.log(`Invalid input, please try again. Invalid values: ${invalid.join(", ")}`);
                value = null;
            }

            break;
        }

        if (value == "") {
            value = null;
        }
    }

    if (typeof value == 'string') {
        return valuesMap[value];
    } else {
        return value.map((val) => valuesMap[val]);
    }
}

const main = async () => {
    const allImages = await prisma.images.findMany();

    const allObjects = await prisma.objects.findMany({
        where: {
            NOT: {
                id: {
                    in: allImages.map((img) => img.file)
                }
            }
        }
    });

    console.log(`Found ${allObjects.length} objects to sync`);

    for (const object of allObjects) {
        const url = await supabase.storage.from('nekos-api').createSignedUrl(object.name, 60 * 5);

        console.log("IMAGE URL:", highlight(url.data.signedUrl))

        if (await inputSelect("Add to database?", ["yes", "no", "y", "n"]) in ["no", "n"]) {
            continue;
        }

        var nsfw = await inputSelect(
            "NSFW", 
            [
                { label: "sfw", value: "sfw" }, 
                { label: "q", value: "questionable" }, 
                { label: "nsfw", value: "nsfw" }
            ]
        );

        console.log("Loading categories...")
        const categories = await prisma.categories.findMany();

        var selectedCategories = await inputSelect(
            "Category",
            categories.map((cat) => ({ label: cat.name, value: cat.id })),
            true
        );

        var sourceName = await prompt("Source name: ");
        var sourceUrl = await prompt("Source URL: ");

        console.log("Getting image dimensions...")

        const { height, width } = await probe(url.data.signedUrl);

        console.log(`${width}x${height}`)

        console.log("Adding to database...")

        await prisma.images.create({
            data: {
                file: object.id,
                nsfw: nsfw,
                categories: selectedCategories,
                source_name: sourceName == "" ? null : sourceName,
                source_url: sourceUrl == "" ? null : sourceUrl,
                height: height,
                width: width
            }
        })

        console.log("Added to database!")

        await prompt('Press enter to continue...');
        console.log("")
    }
}

main()