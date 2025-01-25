import csv
from typing import NamedTuple, List
from difflib import SequenceMatcher
from math import sqrt
import random 

SOTD = NamedTuple("SOTD", [('number', int),
                           ('song_name', str),   
                           ('album_name', str),
                           ('artist_name', str),
                           ('genres', str),
                           ('date', int),
                           ('pop', int),
                           ('dance', float),
                           ('energy', float),
                           ('key', int),
                           ('speech', float),
                           ('accoust', float),
                           ('inst', float),
                           ('live', float),
                           ('tempo', float)]) 

WEIGHTS = {'genre': 8.0,   
           'artist': 8.0,  
           'numeric': 3.0,
           'tempo': 1.0,
           'pop': 2.0,     
           'dance': 0.5,
           'energy': 1.0,
           'speech': 0.5,
           'accoust': 1.5,
           'inst': 0.5,
           'live': 0.5}

def str_to_float(s:str) -> float:
    return float(s)

def str_to_int(s:str) -> int:
    return int(s)

def date_year(s: str) -> str:
    return s[:4]

def file_reader(filename: str) -> List[SOTD]:
    list_sotd = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        
        for row_data in reader:
            sotd = SOTD(str_to_int(row_data[14]), row_data[0], row_data[1], row_data[2], row_data[5], 
                        str_to_int(date_year(row_data[3])), (str_to_int(row_data[4])/100), str_to_float(row_data[6]), 
                        str_to_float(row_data[7]), str_to_int(row_data[8]), str_to_float(row_data[9]), 
                        str_to_float(row_data[10]), str_to_float(row_data[11]), str_to_float(row_data[12]), 
                        str_to_float(row_data[13]))
            list_sotd.append(sotd)

    return list_sotd

def genre_similarity(g1: str, g2:str) -> float:
    genres1 = sorted(genre.strip() for genre in g1.split(','))
    genres2 = sorted(genre.strip() for genre in g2.split(','))
    
    if genres1 == genres2:
        return 1.0 
    
    genre_similarity = SequenceMatcher(None, ','.join(genres1), ','.join(genres2)).ratio()
    return genre_similarity

def artist_similarity(a1: str, a2: str) -> float:
    artists1 = set(artist.strip() for artist in a1.split(','))
    artists2 = set(artist.strip() for artist in a2.split(','))

    if artists1 == artists2:
        return 1.0 

    # Specific artist conditions
    special_cases = [
        ({'Adrianne Lenker'}, {'Big Thief'}),
        ({'Big Thief'}, {'Adrianne Lenker'}),
        ({'alex_g_offline'}, {'Alex G'}),
        ({'Alex G'}, {'alex_g_offline'})]
    
    if any(artists1 == case[0] and artists2 == case[1] or artists1 == case[1] and artists2 == case[0] for case in special_cases):
        return 1.0

    # checkin the boys
    boygenius_group = {'boygenius', 'Phoebe Bridgers', 'Lucy Dacus', 'Julien Baker'}
    
    if artists1.union(artists2).issubset(boygenius_group):
        return 1.0

    # drain gang check
    dg = {'Bladee', 'Ecco2k', 'Thaiboy Digital', 'Yung Lean'}
    if artists1.union(artists2).issubset(dg):
        return 1.0
    
    similarity = SequenceMatcher(None, ','.join(sorted(artists1)), ','.join(sorted(artists2))).ratio()
    return similarity

def tempo_similarity(t1: float, t2: float) -> float:
    if (t1 - t1*0.1) <= t2 <= (t1 + t1*0.1):
        return 1.0
    else:
        return 0.0

def numeric_similarity(song1: SOTD, song2: SOTD) -> float:
    attributes = ['pop', 'dance', 'energy', 'speech', 'accoust', 'inst', 'live']
    distance = 0.0
    
    for attribute in attributes:
        val1 = getattr(song1, attribute, 0)
        val2 = getattr(song2, attribute, 0)
        weight = WEIGHTS.get(attribute, 1.0)
        distance += weight * (val1 - val2) ** 2

    max_distance = len(attributes) 
    similarity = 1 - (sqrt(distance) / sqrt(max_distance))
    
    return max(0, similarity)

def combined_similarity(song1: SOTD, song2: SOTD) -> float:
    genre_sim = genre_similarity(song1.genres, song2.genres)
    artist_sim = artist_similarity(song1.artist_name, song2.artist_name)
    numeric_sim = numeric_similarity(song1, song2)

    total_sim = (WEIGHTS['genre'] * genre_sim +
                 WEIGHTS['artist'] * artist_sim +
                 WEIGHTS['numeric'] * numeric_sim) / sum(WEIGHTS.values())
    
    return total_sim

def most_similar_songs(song_number: int, list_sotd: List[SOTD], num_similar: int = 7) -> List[SOTD]:
    input_song = next(song for song in list_sotd if song.number == song_number)
    similarities = [
        (song, combined_similarity(input_song, song)) 
        for song in list_sotd if song.number != song_number
    ]
    sorted_songs = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [song for song, _ in sorted_songs[:num_similar]]
