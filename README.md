![Nekos API Banner](https://nekosapi.com/branding/banner.png)

# Nekos API

Nekos API is an open-source, free and public anime images RESTful API (soon bringing GraphQL and WebSockets for webhooks) with more than 13k images and counting.

## Why Nekos API

There are many other APIs that serve anime images and even GIFs, but there are lots of reasons why you would prefer Nekos API over other similar projects:

- 100% free forever. You don't need to pay a cent to use the whole API and get thousands of images!
- Open source. The code you see here is exactly what it's running on our server. There is not a single modification (ignoring .env files obviously).
- Thousands of images. At the time of writing we are already serving +13400 images! We try to add even more regularly, so you probably won't find the same image twice (unless you store its ID).
- Advanced API. Probably the most advanced anime images API out there. This may make it difficult to use for beginners, but once you learn how to use it you'll understand why we say this. Included resources, relationships, and embeddable API endpoints are just some of the features that only Nekos API provides.
- Frequent updates. We bring updates almost weekly, so you'll never find out that what you need is not provided by the API.
- 24/7 support on [our Discord server](https://discord.gg/PgQnuM3YnM). You'll find someone who wants to help you in our Discord server no matter how dumb or silly you think that your question is!
- Officially supported API wrappers. Do you want something advanced, easy, and fast? Our official API wrappers will help you seamlessly integrate the API in your project!

## Documentation

The documentation can be found at [our website](https://nekosapi.com/docs/).

## Development setup

First, clone the repository:

```
git clone https://github.com/Nekos-API/Nekos-API
cd Nekos-API
```

Next, run this script in the root folder of the project. You'll need to have [Python 3](https://python.org), [Poetry](https://python-poetry.org), [Node.js](https://nodejs.org) and [pNPM](https://pnpm.io) installed to run it.

```
cd api
poetry shell
poetry install
deactivate

cd ../docs
pnpm install

cd ../images-admin
pnpm install

cd ../website
pnpm install

cd ../
```

Now, you need to set up the environment variables for each subproject: `api`, `docs`, `images-admin`, and `website`. You don't need to set up those you won't use.

Each folder has a documented `.env.example` file that you can use as a template. Check each folder's README and `.env.example` file for more information.