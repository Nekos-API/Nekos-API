import { Redis } from '@upstash/redis';

const client = new Redis({
    url: process.env.UPSTASH_URL,
    token: process.env.UPSTASH_TOKEN,
});

export default client