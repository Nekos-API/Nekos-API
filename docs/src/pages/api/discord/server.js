export default async function handler(req, res) {
    const { invite_code } = req.query;

    const r = await fetch(`https://discord.com/api/v10/invites/${encodeURIComponent(invite_code)}?with_counts=true`, {
        headers: {
            // Authorization: `Bot ${process.env.DISCORD_BOT_TOKEN}`
        }
    });

    const server = await r.json();
    const { approximate_member_count, approximate_presence_count } = server;

    res.json({
        members: {
            online: approximate_presence_count,
            total: approximate_member_count
        }
    })
}