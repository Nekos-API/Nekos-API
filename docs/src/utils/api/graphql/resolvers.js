import getImage from "./resolvers/getImage";
import getRandomImages from "./resolvers/getRandomImages";
import getArtist from "./resolvers/getArtist";
import getArtists from "./resolvers/getArtists";
import getArtistImages from "./resolvers/getArtistImages";

export default {
    Query: {
        getImage,
        getRandomImages,
        getArtist,
        getArtists,
        getArtistImages
    },
};
