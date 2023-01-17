import pygame
from settings import *
from entity import Entity
from support import import_folder
from typing import Tuple
from player import Player

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites) -> None:
        
        # general setup
        super().__init__(groups, obstacle_sprites)
        self.animation_speed = 0.15
        self.sprite_type = "enemy"
        
        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations['idle'][0]
        
        # movement
        adjusted_pos = (pos[0] + 32, pos[1] + 32) # calculates the centre of the square
        self.rect = self.image.get_rect(center=adjusted_pos) # places the enemy at the previously determined center position
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = ENEMY_DATA[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_type = monster_info['attack_type']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.max_follow_distance = monster_info['max_follow_distance']
        self.spawn_pos = adjusted_pos
        
        # player interactions
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 600
    
    def import_graphics(self, monster_name: str) -> None:
        """Imports the monster assets for a given monster (by their name)

        Args:
            monster_name (str): The name of the monster that we want to import assets for
        """        
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/monsters/{monster_name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player: Player) -> tuple[float, float]:
        """Gets are returns the distance and direction to the player as a tuple.

        Args:
            player (Player): The current player object.

        Returns:
            tuple[float, float]: a tuple containing the distance and direction from the player in that order.
        """        
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        
        return(distance, direction)

    def get_status(self, player: Player) -> None:
        """Updates the status of the enemy in relation to the player.

        Args:
            player (Player): The player object in the scene.
        """        
        distance = self.get_player_distance_direction(player)[0]
        
        if distance >= self.max_follow_distance:
            self.status = "idle" # Move back to spawn pos
        elif distance <= self.attack_radius and self.can_attack:
            self.status = "attack"
            self.attack_time = pygame.time.get_ticks()
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = 'idle'
    
    def actions(self, player: Player) -> None:
        """Mini state machine for the actions the enemy can take.

        Args:
            player (Player): The player object in the scene.
        """        
        if self.status == 'attack':
            # print("attack")
            pass
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        elif self.status == 'idle':
            self.direction = pygame.math.Vector2()
    
    def animate(self) -> None:
        """Overwritten from the entity base class
        """
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
    def cooldowns(self) -> None:
        """Function that checks to see if the attack cooldown has been completed
        """
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    
    def update(self) -> None:
        """Should run every frame to update the enemy position. This is a general function for all sprites.
        """        
        self.move(self.speed)
        self.animate()
        self.cooldowns()
    
    def enemy_update(self, player: Player) -> None:
        """Enemy specific update function that updates the enemy status and runs the action state-machine.
        Should also be run once per frame.

        Args:
            player (Player): The player object in the scene.
        """        
        self.get_status(player)
        self.actions(player)