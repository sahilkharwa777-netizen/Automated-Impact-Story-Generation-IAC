import hashlib


def anonymize_data(data):

    data["participant_id"] = (
        data["name"]
        .apply(
            lambda x:
            hashlib.sha256(
                x.encode()
            ).hexdigest()[:10]
        )
    )


    data = data.drop(
        "name",
        axis=1
    )


    return data