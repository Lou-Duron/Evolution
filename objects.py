#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random
import numpy as np

class SQUARE():
    EMPTY = 0
    FOOD = 1
    WATER = 2
    OBSTACLES = 3
    ORG = 4

S = SQUARE()

class World:

    def __init__(self, size, max_steps, food_nb, lacs_nb, obst_nb,
                 org_nb, max_nrj, vision, genomes):
        self.size = size
        self.food_nb = food_nb
        self.lacs_nb = lacs_nb
        self.obst_nb = obst_nb
        self.org_nb = org_nb
        self.org_max_nrj = max_nrj
        self.org_vision = vision
        self.max_steps = max_steps
        self.generation = 0
        self.setup_world(genomes)

    def update(self):
        self.steps -= 1
        for org in self.org:
            org.update(self)
        if self.steps <= 0:
            self.generation += 1
            self.setup_world(np.zeros((self.org_nb)))

    def setup_world(self, genomes):
        self.steps = self.max_steps
        self.grid = np.zeros((self.size, self.size))
        self.init_foods(self.food_nb)
        self.init_lacs(self.lacs_nb)
        self.init_obstacles(self.obst_nb)
        self.init_organisms(genomes)

    def init_foods(self, nb):
        r = np.random.randint(0, self.size, (nb,2))
        food = []
        for el in r:
            food.append([el[0], el[1]])
            self.grid[el[0], el[1]] = S.FOOD
        self.food = np.array(food)

    def init_lacs(self, nb):
        r = np.random.randint(0, self.size, (nb,2))
        self.lacs = []
        for el in r:
            width = random.randint(10,100)
            height = random.randint(10,100)
            self.lacs.append([el[0], el[1], width, height])
            self.grid[el[0]:el[0] + width, el[1]:el[1]+height] = S.WATER

    def init_obstacles(self, nb):
        r = np.random.randint(0, self.size, (nb,2))
        self.obst = []
        for el in r:
            width = random.randint(10,100)
            height = random.randint(10,100)
            self.obst.append([el[0], el[1], width, height])
            self.grid[el[0]:el[0] + width, el[1]:el[1]+height] = S.OBSTACLES

    def init_organisms(self, genomes):
        i = 0
        self.org = []
        while i < len(genomes):
            pos = np.random.randint(0, self.size, (2))
            if self.grid[pos[0], pos[1]] == S.EMPTY:
                self.org.append(Organism(pos[0], pos[1], genomes[i], self.org_max_nrj, self.org_vision))
                self.grid[pos[0], pos[1]] = S.ORG
                i += 1

class Organism():

    def __init__(self, x, y, genome, max_nrj, vision):
        self.x = x
        self.y = y
        self.vision = vision
        self.energy = max_nrj
        self.fitness = 0
        self.genome = genome

    def update(self, world):
        self.energy -= 1
        if self.energy <= 0 or world.grid[self.x, self.y] == S.WATER:
            world.org.remove(self)
        neighbours = self.get_neighbours(world)
        for n in neighbours:
            if world.grid[n[0], n[1]] == S.WATER:
                self.energy = world.org_max_nrj
            if world.grid[n[0], n[1]] == S.FOOD:
                self.energy += 1
                self.fitness += 1
                world.grid[n[0], n[1]] = S.EMPTY
                world.food = world.food[np.where(world.food != [n[0],n[1]])].reshape(2,-1)
        
    
    def get_neighbours(self, world):
        n = []
        if self.x > world.size:
            n.append([self.x + 1, self.y])
        if self.x < 0:
            n.append([self.x - 1, self.y])
        if self.y > world.size:
            n.append([self.x , self.y + 1])
        if self.y < 0:
            n.append([self.x, self.y - 1])
        return n

    def get_inputs(self, grid):
        inputs = np.zeros(11)
        inputs[0] = self.x
        inputs[1] = self.y
        inputs[10] = self.energy
        for i, x in enumerate(range(self.x + self.vision, self.x + 1)):
            for j in range(-1, 2, 2):
                if grid[x*j, self.y] == S.FOOD:
                    inputs[2] = i / self.vision
                if grid[x*j, self.y] == S.WATER:
                    inputs[4] = i / self.vision
                if grid[x*j, self.y] == S.OBSTACLES:
                    inputs[6] = i / self.vision
                if grid[x*j, self.y] == S.WATER:
                    inputs[8] = i / self.vision
        for i, y in enumerate(range(self.y + self.vision, self.y + 1)):
            for j in range(-1, 2, 2):
                if grid[self.x, y*j] == S.FOOD:
                    inputs[3] = i / self.vision
                if grid[self.x, y*j] == S.WATER:
                    inputs[5] = i / self.vision
                if grid[self.x, y*j] == S.OBSTACLES:
                    inputs[7] = i / self.vision
                if grid[self.x, y*j] == S.WATER:
                    inputs[9] = i / self.vision
        return inputs

    
    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x >= 0 and new_x <= world.size:
            self.x = new_x
        if new_y >= 0 and new_y <= world.size:
            self.y = new_y

class Brain():

    def __init__(self, genome):
        pass  