import copy
import csv
import random
from typing import Optional
from random import randint


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

    poblation_size = 1500
    generations = 1000
    poblation = generate_tables(copy.copy(alll), poblation_size, destination)
    zzz = []
    best_of_all = None
    for generation in range(generations):
        # print(f"Generation: {generation + 1}")
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
