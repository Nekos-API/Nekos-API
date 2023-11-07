export default async function handler(req, res) {
    const { user_id } = req.query;
    BigInt(user_id);

    const r = await fetch(`https://discord.com/api/v10/users/${user_id}`, {
        headers: {
            Authorization: `Bot ${process.env.DISCORD_BOT_TOKEN}`,
        },
    });

    const user = await r.json();
    const avatar_hash = user.avatar;

    res.redirect(
        307,
        avatar_hash != null
            ? `https://cdn.discordapp.com/avatars/${user_id}/${avatar_hash}?size=512`
            : "/imgs/discord-default-avatar.png"
    );
}
