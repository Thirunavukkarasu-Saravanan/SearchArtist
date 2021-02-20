import json
from fuzzywuzzy import fuzz

cached_data = {"data": [], "count": 0}
file_path = "data.json"  # "fake_band_names_mit.txt"
fuzzy_ratio_adjust = 60


def __fetch_all_artist_names(load_from_cache=True):
    ''' Method to fetch all artist from JSON
    '''
    artists = None
    # reload from cache
    if load_from_cache and cached_data["count"] > 0:
        return cached_data["data"]

    with open(file_path, "r") as seeker:
        artists = json.load(seeker)

    if artists is None:
        return []
    else:
        data = list(map(lambda artist: artist["name"], artists))
        cached_data["data"] = data
        cached_data["count"] = len(data)
        return data


def __fetch_limited_artist(match_name: str, skip: int = 0, limit: int = 50):
    ''' Method to fetch all artist based on search criteria (name, number of artists) 
    '''
    data = []
    artists = __fetch_all_artist_names()
    if len(artists) <= skip:
        return data

    for artist in artists:

        if limit == 0:
            return data

        if match_name == artist or match_name in artist:
            if skip > 0:
                skip -= 1
                continue
            data.append(artist)
            limit -= 1

    return data


def __fetch_similar_artist(match_name: str, skip: int = 0, limit: int = 50, existing_data=None):
    ''' Method to fetch all artist based on search criteria using fuzzylogic (name, number of artists) 
    '''
    data = []
    artists = __fetch_all_artist_names()

    if len(artists) <= skip:
        return data

    for artist in artists:

        if limit == 0:
            return data

        if (
            existing_data is not None
            and len(existing_data) > 0
            and artist in existing_data
        ):
            continue

        ratio = fuzz.ratio(artist, match_name)
        if ratio >= fuzzy_ratio_adjust:
            if skip > 0:
                skip -= 1
                continue
            data.append(artist)
            limit -= 1

    return data


def fetch_artist(match_name: str, skip: int = 0, limit: int = 50):
    ''' Method to fetch all artist based on search criteria 
    '''
    data = []
    all_data_count = 0
    if match_name is None or match_name == "":
        data = __fetch_all_artist_names()
        all_data_count = len(data)
        return (data[skip:limit], all_data_count)
    else:
        all_data_count = len(__fetch_all_artist_names())
    print(match_name, skip, limit)

    data = __fetch_limited_artist(match_name, skip, limit)

    return (data, all_data_count)

    if len(data) < limit or skip > len(data):
        skip += len(data)
        limit -= len(data)
        extra_data = __fetch_similar_artist(match_name, skip, limit, data)
        if extra_data is not None and len(extra_data) > 0:
            data += extra_data
