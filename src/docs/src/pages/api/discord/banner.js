import sharp from "sharp";

export default async function handler(req, res) {
    const { user_id } = req.query;
    BigInt(user_id);

    const r = await fetch(`https://discord.com/api/v10/users/${user_id}`, {
        headers: {
            Authorization: `Bot ${process.env.DISCORD_BOT_TOKEN}`,
        },
    });

    const user = await r.json();
    const banner_hash = user.banner;

    res.redirect(
        307,
        banner_hash != null
            ? `https://cdn.discordapp.com/banners/${user_id}/${banner_hash}?size=512`
            : "/imgs/discord/default-banner.png"
    );
}
