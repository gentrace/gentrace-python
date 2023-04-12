from datetime import datetime


def to_date_string(time_value):
    return (
        datetime.fromtimestamp(time_value).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"
    )
