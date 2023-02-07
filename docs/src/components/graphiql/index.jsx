import * as React from "react";
import Link from "next/link";
import Head from "next/head";
import GraphiQL from "graphiql";
import { useExplorerPlugin } from '@graphiql/plugin-explorer';

import styles from "./index.module.css";
import "graphiql/graphiql.css";
import '@graphiql/plugin-explorer/dist/style.css';

const defaultQuery = /* GraphQL */ `
# Welcome to Nekos API GraphQL API!
#
# You can use this editor to test your queries,
# read the documentation and save code snippets.
#
# Here is an example:

query ExampleQuery($limit: Int!) {
  images: getRandomImages(limit: $limit) {
    id
    url
  }
}

# To run this example either:
# - Ctrl/Cmd + Enter
# - Click on the pink run button
`.trim();

export default function IDE({ }) {
    const [query, setQuery] = React.useState(defaultQuery);
    const explorerPlugin = useExplorerPlugin({
        query,
        onEdit: setQuery,
    });
    return (
        <div style={{
            height: "100vh"
        }}>
            <Head>
                <title>GraphQL Playground - Nekos API</title>
            </Head>
            <GraphiQL
                fetcher={async (graphQLParams) => {
                    const data = await fetch("/api/graphql", {
                        method: "POST",
                        headers: {
                            Accept: "application/json",
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(graphQLParams),
                        credentials: "same-origin",
                    });
                    return data.json().catch(() => data.text());
                }}
                defaultQuery={defaultQuery}
                variables={`{\n  "limit": 5\n}`}
                query={query}
                onEditQuery={setQuery}
                plugins={[explorerPlugin]}
            >
                <GraphiQL.Logo>
                    <Link href="/" className="hover:opacity-90 flex flex-row items-center gap-2 text-sm">
                        <img src="/logo/black.png" className="h-6 w-6" />
                        <span className={styles.logo}>Nekos API</span>
                    </Link>
                </GraphiQL.Logo>
            </GraphiQL>
        </div>
    )
}