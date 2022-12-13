import pygame
from settings import *
from support import *
from entity import Entity
from typing import Union

class Player(Entity):
    def __init__(
            self,
            pos,
            groups,
            obstacle_sprites,
            create_attack,
            destroy_attack) -> None:
        super().__init__(groups, obstacle_sprites)
        # Sprite vars
        self.image = pygame.image.load(
            '../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.invulnerable = False

        # Graphics setup
        self.import_player_assets()
        self.status = 'down_idle'

        # Movement vars
        self.roll_speed_modifier = 1.4
        self.post_roll_speed_modifier = 0.6

        # Attack vars
        self.attacking = False
        self.attack_active = 400
        self.attack_time = None

        # Weapon vars
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.can_switch_weapons = True
        self.weapon_switch_time = None
        self.weapon_switch_dureation_cooldown = 200

        # Rolling vars
        self.rolling = False
        self.roll_used = False
        self.roll_active = 300
        self.roll_cooldown = 300
        self.roll_time = None
        self.roll_end_time = None

        # stats
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'speed': PLAYER_SPEED}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

    def import_player_assets(self) -> None:
        """Imports the players assets from the player graphics folder and puts them
        in the self.animations array.
        """
        character_path = "../graphics/player/"
        self.animations = {
            'down': [],
            'down_attack': [],
            'down_idle': [],
            'down_roll': [],
            'left': [],
            'left_attack': [],
            'left_idle': [],
            'left_roll': [],
            'right': [],
            'right_attack': [],
            'right_idle': [],
            'right_roll': [],
            'up': [],
            'up_attack': [],
            'up_idle': [],
            'up_roll': []}
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(
                character_path + animation)

    def input(self) -> None:
        """Process keyboard inputs.
        """
        keys = pygame.key.get_pressed()

        # make sure that if we're rolling we keep momentum, but when attacking
        # we want to reset it
        if self.rolling:
            if self.direction.x == 0 and self.direction.y == 0:
                status = self.status.split("_")[0]
                if status == "left":
                    self.direction.x = -1
                elif status == "right":
                    self.direction.x = 1
                elif status == "up":
                    self.direction.y = -1
                elif status == "down":
                    self.direction.y = 1
            return

        self.direction.x = 0
        self.direction.y = 0

        if self.attacking:
            return

        # Attack:
        if keys[pygame.K_f]:
            self.attacking = True
            self.create_attack()
            self.attack_time = pygame.time.get_ticks()
            return

        # Movement:
        if keys[pygame.K_UP]:
            self.direction.y -= 1
            self.status = "up"
        if keys[pygame.K_DOWN]:
            self.direction.y += 1
            self.status = "down"

        if keys[pygame.K_LEFT]:
            self.direction.x -= 1
            self.status = "left"
        if keys[pygame.K_RIGHT]:
            self.direction.x += 1
            self.status = "right"

        # Dodge roll:
        if keys[pygame.K_d] and not self.roll_used:
            self.rolling = True
            self.invulnerable = True
            self.roll_time = pygame.time.get_ticks()

        # Weapon switch:
        if keys[pygame.K_q] and self.can_switch_weapons:
            self.can_switch_weapons = False
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon_index += 1
            self.weapon_index %= len(WEAPON_DATA)
            self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

    def get_status(self) -> None:
        """Changes the player status to reflect the current input.
        """
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status and 'roll' not in self.status:
                self.status += "_idle"

        if self.attacking:
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += "_attack"

        if self.rolling:
            if 'roll' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_roll')
                else:
                    self.status += "_roll"

    def cooldowns(self) -> None:
        """Function that checks to see if the attack or roll cooldown has been completed.
        """
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_active:
                self.attacking = False
                self.status = self.status.replace('_attack', '')
                self.destroy_attack()

        if self.rolling:
            if current_time - self.roll_time >= self.roll_active:
                self.rolling = False
                self.status = self.status.replace('_roll', '')
                self.roll_used = True
                self.invulnerable = False
                self.roll_end_time = current_time

        if self.roll_used:
            if current_time - self.roll_end_time >= self.roll_cooldown:
                self.roll_used = False

        if not self.can_switch_weapons:
            if current_time - self.weapon_switch_time >= self.weapon_switch_dureation_cooldown:
                self.can_switch_weapons = True

    def animate(self) -> None:
        """Selects and displays the right frame of the current animation.
        """
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += PLAYER_ANIMATION_SPEED
        self.frame_index = self.frame_index % len(animation)

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def move(self, speed: Union[int, float]):
        """Takes into account if the player is rolling or not before running the move command

        Args:
            speed (Union[int, float]): Speed of the player.
        """    
        speed = self.speed
        if self.rolling:
            speed *= self.roll_speed_modifier

        if self.roll_used:
            speed *= self.post_roll_speed_modifier
        super().move(speed)
    
    def update(self) -> None:
        """Is run every frame, gets input and updates movement.
        """
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
