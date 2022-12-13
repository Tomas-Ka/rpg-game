import pygame
from settings import *
from support import *
from entity import Entity
from player import Player

# TODO THIS FILE IS IN PREPARATION FOR NETWORKING, AND NOTHING WILL BE DONE WITH IT FOR A WHILE

class NetworkedPlayer(Player):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(pos, groups, obstacle_sprites, create_attack, destroy_attack)
    
    def listen_network(self):
        # get status packet from network
        
        # attack input, direction vector, dodge input and weapon switch input
        # also gets position and stores it in networked_position
        self.networked_position = (0, 0)
        pass

    def move(self):
        self.hitbox.x, self.hitbox.y = self.networked_position
        
    
    def update(self) -> None:
        """Overwrite of the Player update function
        """
        self.listen_network()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move()