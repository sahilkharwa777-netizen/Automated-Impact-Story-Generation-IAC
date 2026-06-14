def filter_consent(data):

    approved_data = data[
        data["consent"] == "yes"
    ]

    return approved_data