require("dotenv").config();

const { PrismaClient } = require("@prisma/client");
const { createClient } = require("@supabase/supabase-js");

const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_ANON_SUPABASE_KEY
);

const prisma = new PrismaClient();

async function main() {
    const files = await prisma.$queryRaw`SELECT * FROM storage.objects WHERE NOT name LIKE '%' || id || '%'`

    let i = 1;
    let errors = 0;

    console.log(`Found ${files.length} files to rename`)

    for (const file of files) {
        const { data, error } = await supabase
            .storage
            .from('nekos-api')
            .move(file.name, `images/${file.id}.${file.name.split('.').at(-1)}`)

        if (error) {
            console.log(`Error - ${file.id} - (${i}/${files.length})`)
            error++
        } else {
            console.log(`Renamed ${file.name} > images/${file.id}.${file.name.split('.').at(-1)} - (${i}/${files.length})`)
        }

        i++
    }

    console.log(`Renamed ${files.length - errors} files. ${errors} files could not be renamed.`)
}

main();