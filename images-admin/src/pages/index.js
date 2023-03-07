import React from "react";

export default function Home() {
    const [loading, setLoading] = React.useState(false);
    const [image, setImage] = React.useState();
    const [ageRating, setAgeRating] = React.useState("sfw");

    const getNextImage = async () => {
        const res = await fetch(
            process.env.NEXT_PUBLIC_API_BASE +
                "/v2/images?filter[verificationStatus]=not_reviewed&page[limit]=1&sort=-created_at",
            {
                headers: {
                    Accept: "application/vnd.api+json",
                },
                credentials: "include",
            }
        );
        const json = await res.json();
        return json.data[0];
    };

    const setVerification = async (status) => {
        image.attributes.ageRating = ageRating;

        const vres = await fetch(
            process.env.NEXT_PUBLIC_API_BASE +
                "/v2/images/" +
                image.id +
                "/verification?status=" +
                status,
            {
                method: "POST",
                headers: {
                    Accept: "application/vnd.api+json",
                },
                credentials: "include",
            }
        );
        const ares = await fetch(
            process.env.NEXT_PUBLIC_API_BASE + "/v2/images/" + image.id,
            {
                method: "PATCH",
                headers: {
                    Accept: "application/vnd.api+json",
                    "Content-Type": "application/vnd.api+json",
                },
                credentials: "include",
                body: JSON.stringify({ data: image }),
            }
        );
        if (vres.status != 200) {
            alert("Could not set verification status!");
            return false;
        }
        if (ares.status != 200) {
            alert("Could not set age rating!");
            return false;
        }
        return true;
    };

    React.useEffect(() => {
        setLoading(true);
        getNextImage().then((data) => {
            setImage(data);
            setLoading(false);
        });
    }, []);

    return (
        <div className="h-screen w-screen flex flex-col items-center p-10">
            <div className="flex flex-col w-full max-w-sm h-full relative gap-10 items-center">
                <div>ID: {image && !loading ? image.id : "Loading..."}</div>
                <div className="flex-1 flex flex-col items-center justify-center w-full">
                    <img
                        className="flex-1 w-full h-full rounded object-contain bg-black drop-shadow"
                        src={image && !loading ? image.attributes.file : ""}
                    />
                </div>
                <div className="flex flex-row gap-5 items-center">
                    <div>
                        <input
                            type="radio"
                            name="age_rating"
                            value="sfw"
                            id="sfw"
                            defaultChecked={true}
                            onSelect={() => {
                                setAgeRating("sfw");
                            }}
                        />
                        <label for="sfw">SFW</label>
                    </div>
                    <div>
                        <input
                            type="radio"
                            name="age_rating"
                            value="questionable"
                            id="questionable"
                            onSelect={() => {
                                setAgeRating("questionable");
                            }}
                        />
                        <label for="questionable">Questionable</label>
                    </div>
                    <div>
                        <input
                            type="radio"
                            name="age_rating"
                            value="suggestive"
                            id="suggestive"
                            onSelect={() => {
                                setAgeRating("suggestive");
                            }}
                        />
                        <label for="suggestive">Suggestive</label>
                    </div>
                    <div>
                        <input
                            type="radio"
                            name="age_rating"
                            value="borderline"
                            id="borderline"
                            onSelect={() => {
                                setAgeRating("borderline");
                            }}
                        />
                        <label for="borderline">Borderline</label>
                    </div>
                    <div>
                        <input
                            type="radio"
                            name="age_rating"
                            value="explicit"
                            id="explicit"
                            onSelect={() => {
                                setAgeRating("explicit");
                            }}
                        />
                        <label for="explicit">Explicit</label>
                    </div>
                </div>
                <div className="flex flex-row gap-2.5 items-center">
                    {loading ? (
                        <div>Loading...</div>
                    ) : (
                        <>
                            <button
                                className="flex-1 p-2.5 leading-none rounded text-white whitespace-nowrap bg-red-400"
                                onClick={async () => {
                                    setLoading(true);
                                    const success = await setVerification(
                                        "declined"
                                    );
                                    if (!success) {
                                        setLoading(false);
                                        return;
                                    }

                                    setImage(await getNextImage());
                                    setLoading(false);
                                }}
                            >
                                DECLINED
                            </button>
                            <button
                                className="flex-1 p-2.5 leading-none rounded text-white whitespace-nowrap bg-yellow-400"
                                onClick={async () => {
                                    setLoading(true);
                                    const success = await setVerification(
                                        "on_review"
                                    );
                                    if (!success) {
                                        setLoading(false);
                                        return;
                                    }

                                    setImage(await getNextImage());
                                    setLoading(false);
                                }}
                            >
                                ON REVIEW
                            </button>
                            <button
                                className="flex-1 p-2.5 leading-none rounded text-white whitespace-nowrap bg-green-400"
                                onClick={async () => {
                                    setLoading(true);
                                    const success = await setVerification(
                                        "verified"
                                    );
                                    if (!success) {
                                        setLoading(false);
                                        return;
                                    }

                                    setImage(await getNextImage());
                                    setLoading(false);
                                }}
                            >
                                VERIFIED
                            </button>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
