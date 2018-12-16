import mesa.agent
import numpy as np
import random

import simulation_parameters

class WarriorAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hp = 10
        self.ENEMY_SCANNING_RADIUS = simulation_parameters.VISION_RANGE # promień widzenia przeciwników
        self.FLOCKING_RADIUS = simulation_parameters.FLOCKING_RADIUS # promień widzenia swoich
        self.SEPARATION_DISTANCE = simulation_parameters.SEPARATION_DISTANCE # jaki dystans chce zachować od innych w oddziale
        self.COHERENCE_FACTOR = simulation_parameters.COHERENCE_FACTOR
        self.MATCH_FACTOR = simulation_parameters.MATCH_FACTOR
        self.SEPARATION_FACTOR = simulation_parameters.SEPARATION_FACTOR
        self.ENEMY_POSITION_FACTOR = simulation_parameters.ENEMY_POSITION_FACTOR

    def step(self):
        if self.hp <= 0:
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.move()

    # ostateczny wektor prędkości otrzymujemy normalizując wektor prędkości z funkcji niżej i mnożąc go przez szybkość
    # danego typu agenta (skalarną) parametryzowaną w pliku konfiguracyjnym
    def move(self):
        velocity_vector = self.calculate_velocity_vector()
        normalised_velocity_vector = velocity_vector / np.linalg.norm(velocity_vector)
        end_point = self.pos + normalised_velocity_vector * self.movement_speed
        self.model.space.move_agent(self, end_point)

    def calculate_velocity_vector(self):
        visible_enemies = self.scan_for_enemies()
        visible_allies = self.scan_for_allies()

        # wektor prędkości przed normalizacją - kombinacja liniowa wektorów z poszczególnych reguł o współczynnikach
        # równych ich wagom (parametryzowanych w pliku konfiguracyjnym)
        velocity_vector = (self.coherence_vector(visible_allies) * self.COHERENCE_FACTOR +
                           self.match_vector(visible_allies) * self.MATCH_FACTOR +
                           self.separate_vector(visible_allies) * self.SEPARATION_FACTOR +
                           self.enemy_position_vector(visible_enemies) * self.ENEMY_POSITION_FACTOR)

        return velocity_vector

    def scan_for_allies(self):
        warriors_in_flocking_radius = self.model.space.get_neighbors(self.pos, self.FLOCKING_RADIUS, False)
        allies_in_range = []
        for warrior in warriors_in_flocking_radius:
            if warrior.type == self.type:
                allies_in_range.append(warrior)
        return allies_in_range

    def scan_for_enemies(self):
        warriors_in_range = self.model.space.get_neighbors(self.pos, self.ENEMY_SCANNING_RADIUS, False)
        enemies_in_range = []
        for warrior in warriors_in_range:
            if warrior.type != self.type:
                enemies_in_range.append(warrior)
        return enemies_in_range

    def coherence_vector(self, visible_allies):
        vector = np.zeros(2)
        for ally in visible_allies:
            vector += self.model.space.get_heading(self.pos, ally.pos)
        vector /= len(visible_allies)
        return vector

    def match_vector(self, visible_allies):
        vector = np.zeros(2)
        return vector

    def separate_vector(self, visible_allies):
        vector = np.zeros(2)
        return vector

    def enemy_position_vector(self, visible_enemies):
        vector = np.zeros(2)
        return vector



    # def move(self):
    #     if self.type == 'blue':
    #         position = np.array([-1, 0.0])
    #     elif self.type == 'red':
    #         position = np.array([1, 0.0])
    #     new_pos = self.pos + position
    #     new_cell_agents = self.model.space.get_neighbors(new_pos, 0)
    #
    #     if not self.model.space.out_of_bounds(new_pos):
    #         if len(new_cell_agents) == 0:
    #             self.model.space.move_agent(self, new_pos)
    #         else:
    #             self.attack()

    # def attack(self):
    #     if self.type == 'blue':
    #         position = np.array([-1, 0.0])
    #     elif self.type == 'red':
    #         position = np.array([1, 0.0])
    #     new_pos = self.pos + position
    #     cellmates = self.model.space.get_neighbors(new_pos, 2.0)
    #     enemy = random.choice(cellmates)
    #     enemy.hp -= 1


class RedWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'red'
        self.movement_speed = simulation_parameters.RED_MOVEMENT_SPEED

class BlueWarrior(WarriorAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'blue'
        self.movement_speed = simulation_parameters.BLUE_MOVEMENT_SPEED