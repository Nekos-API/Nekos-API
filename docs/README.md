# Nekos API

Open-source free public anime images API. [Join our Discord server](https://discord.gg/PgQnuM3YnM).

## Installation

Clone the repository and install the dependencies.

```bash
git clone https://github.com/Nekidev/Nekos-API.git
cd Nekos-API
pnpm install
```

Set the environment variables. (You need a [Supabase](https://supabase.com) project for this)

- `NEXT_PUBLIC_SUPABASE_KEY` - Supabase project's public key
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase project's URL
- `NEXT_PUBLIC_SUPABASE_BUCKET_NAME` - Supabase project bucket's name

Now just run the project using `pnpm run dev`. It'll start the project on `0.0.0.0:3000`.
