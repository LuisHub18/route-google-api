import copy
import csv
import os
import random
from typing import Optional
from random import randint
from PIL import Image

from dotenv import load_dotenv
import googlemaps
import googlemaps.maps
import googlemaps.distance_matrix
import googlemaps.directions

load_dotenv()

API_KEY = os.getenv('API_KEY')

gmaps = googlemaps.Client(key=API_KEY)

points = {
    "forum": (24.814255766993092, -107.40069025553083),
    "explanada": (24.746813970159995, -107.44599053226524),
    "tec_culiacan": (24.789105722097062, -107.39670416109986),
    "ceiba": (24.79848761268018, -107.4231976034287),
    "catedral": (24.808844787599703, -107.39406046109939),
    "estadio_tomateros": (24.798925888956187, -107.38997589414312),
    "parque_riberas": (24.8130087000168, -107.3891793072115),
    "parque_87": (24.773593786354102, -107.38861731743529),
    "parque_acuatico": (24.80812955949714, -107.40794481027028),
    "plaza_sendero": (24.825444175827357, -107.42706774393118),
    "zoo_culiacan": (24.814883270179752, -107.38424246468543),
    "aeropuerto": (24.767827561065104, -107.47018750115168),
    "splash_club": (24.73110314693567, -107.34740119877841),
    "plaza_san_isidro": (24.755952183680453, -107.40270133061294),
    "jardin_botanico": (24.827146880138784, -107.3859378744943),
    "plaza_pabellon": (24.80403532723677, -107.34387579458584),
    "lomita": (24.789922976167656, -107.393827599695),
    "hospital_general": (24.794560572980007, -107.38695941812759),
    "imss": (24.79741997857549, -107.39011115045139),
    "plaza_ventura": (24.813700381413142, -107.40864841582747),
}


class Point:
    def __init__(self, name: str, prev_point: Optional['Point'] = None, is_blacklisted: bool = False):
        self.name = name
        self.prev_point = prev_point
        self.is_blacklisted = is_blacklisted

    def __repr__(self):
        return f'{self.name} blacklisted: {self.is_blacklisted}'


class Distance:
    def __init__(self, origin: str, destination: str, distance: int):
        self.origin = origin
        self.destination = destination
        self.distance = distance

    def __repr__(self):
        return f'{self.origin} -> {self.destination} ({self.distance}) blacklisted: {self.blacklisted}'


def read_csv(file_path='distances.csv') -> list[Distance]:
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        next(reader)
        return [Distance(origin=row['Origen'], destination=row['Destino'], distance=int(row['Distancia'])) for row in reader]


def generate_tables(points: list[str], times: int, destination: str) -> list[list[str]]:
    tables = []
    for _ in range(times):
        random.shuffle(points)
        tables.append([destination] + points + [destination])
    return tables


def main():
    distances = read_csv()
    alll = list(set([distance.origin for distance in distances]))
    destination = 'lomita'
    alll.remove(destination)

    poblation_size = 150
    generations = 100
    poblation = generate_tables(copy.copy(alll), poblation_size, destination)
    zzz = []
    best_of_all = None
    for generation in range(generations):
        print(f"Generation: {generation + 1}")
        # print("5 Muestras")
        # print(f"{poblation[:5]}...")
        candidates = selection(poblation, 2, distances)
        best = candidates[0]
        zz = fitness(best, distances)
        zzz.append(zz)
        # print(f'Best: {best}')
        # print(f'Fitness: {fitness(best, distances)}')
        # print()
        crossover_res = crossover(candidates, alll)
        new_poblation = mutation(crossover_res, poblation_size, destination)
        if not generation == generations - 1:
            poblation = new_poblation

        if best_of_all is None or zz < fitness(best_of_all, distances):
            best_of_all = best
    print(best_of_all)
    print(fitness(best_of_all, distances))

    points_route = []
    for point in best_of_all:
        points_route.append(points[point])
    print(points_route)

    with (open('ruta.png', 'wb') as f):
        path = googlemaps.maps.StaticMapPath(points=points_route)
        for chunk in googlemaps.maps.static_map(gmaps, size=(1000, 1000), zoom=12, path=path, maptype="roadmap"):
            if chunk:
                f.write(chunk)
    img = Image.open('ruta.png')
    img.show()


def selection(poblation: list[list[str]], fathers_to_select: int, distances: list[Distance]) -> list[list[str]]:
    poblation.sort(key=lambda x: fitness(x, distances))
    return poblation[:fathers_to_select]


def fitness(individue: list[str], distances: list[Distance]) -> int:
    distance = 0
    for i in range(len(individue) - 1):
        origin = individue[i]
        destination = individue[i + 1]
        for distance_obj in distances:
            if distance_obj.origin == origin and distance_obj.destination == destination:
                distance += distance_obj.distance
                break
    return distance


def crossover(candidates: list[list[str]], lugares: list[str]) -> list[str]:
    new_individual = candidates[0].copy()
    for number in lugares:
        random_candidate = random.choice(candidates)
        random_candidate_number_index = random_candidate.index(number)
        new_individual_number_index = new_individual.index(number)
        if random_candidate_number_index == new_individual_number_index:
            continue
        new_individual[random_candidate_number_index], new_individual[new_individual_number_index] = \
            new_individual[new_individual_number_index], new_individual[random_candidate_number_index]
    return new_individual


def mutation(candidate: list[str], poblation_size: int, destination: str) -> list[list[str]]:
    new_poblation = []
    while len(new_poblation) < poblation_size:
        new_poblation.append(mutate(candidate, 0.3, destination))
    return new_poblation


def mutate(individue: list[str], mutation_probability: float, destination: str) -> list[str]:
    def next_index(table: list[str], number: str) -> int:
        random = randint(0, len(table) - 1)
        if table[random] == destination or new_individue[random] == destination:
            return next_index(table, number)
        else:
            return random

    new_individue = individue.copy()
    for i in range(len(new_individue)):
        if new_individue[i] != destination and random.random() < mutation_probability:
            new_index = next_index(new_individue, i)
            new_individue[i], new_individue[new_index] = new_individue[new_index], new_individue[i]
    return new_individue


if __name__ == '__main__':
    main()
