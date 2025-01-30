import bencodepy
import struct
import zstandard

import json

from data4info import identifiers as country_identifiers

DATASET_PATH = "dataset/"


def find_country_identifier(isbn13):
    # TODO: Optimize
    for _ in country_identifiers:
        for identifier in _:
            if str(isbn13).startswith(identifier.replace("-", "")):
                return identifier


def json_dump_dataset(dataset, filename):
    with open(filename, "w") as f:
        f.write(json.dumps(dataset))


def get_dataset_group_by_country(dataset_name, packed_isbns_binary):
    packed_isbns_ints = struct.unpack(f"{len(packed_isbns_binary) // 4}I", packed_isbns_binary)
    data_country = {}
    isbn_streak = True  # Alternate between reading `isbn_streak` and `gap_size`.
    position = 0  # ISBN (without check digit) is `978000000000 + position`.
    for value in packed_isbns_ints:
        if isbn_streak:
            for _ in range(0, value):
                isbn13_without_check = 978000000000 + position
                country_identifier = find_country_identifier(isbn13_without_check)
                if country_identifier in data_country:
                    data_country[country_identifier] += 1
                else:
                    data_country[country_identifier] = 1
                position += 1
        else:  # Reading `gap_size`.
            position += value
        isbn_streak = not isbn_streak

    return [
        {"dataset": dataset_name, "country_identifier": country_identifier, "value": value}
        for country_identifier, value in data_country.items()
    ]


input_filename = "aa_isbn13_codes_20241204T185335Z.benc.zst"
isbn_data = bencodepy.bread(zstandard.ZstdDecompressor().stream_reader(open(input_filename, "rb")))

dataset = []

for prefix, packed_isbns_binary in isbn_data.items():
    dataset_name = prefix.decode()
    new_dataset = get_dataset_group_by_country(dataset_name, packed_isbns_binary)
    json_dump_dataset(new_dataset, f"{DATASET_PATH}/{dataset_name}_country.json")
    dataset += new_dataset

json_dump_dataset(dataset, f"{DATASET_PATH}/all_country.json")
