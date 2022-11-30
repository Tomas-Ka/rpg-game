import pygame
from settings import *
from support import *
from typing import Union


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(groups)
        # Sprite vars
        self.image = pygame.image.load(
            '../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.invulnerable = False

        # Graphics setup
        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        
        # Movement vars
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        self.roll_speed_modifier = 1.4
        self.post_roll_speed_modifier = 0.6
        self.attacking = False
        self.attack_active = 400
        self.attack_time = None
        
        self.rolling = False
        self.roll_used = False
        self.roll_active = 300
        self.roll_cooldown = 300
        self.roll_time = None
        self.roll_end_time = None

        self.obstacle_sprites = obstacle_sprites

        groups[0].camera_pos = pygame.math.Vector2(self.rect.center)


    def import_player_assets(self) -> None:
        """Imports the players assets from the player graphics folder and puts them
        in the self.animations array
        """        
        character_path = "../graphics/player/"
        self.animations = {'down': [], 'down_attack': [], 'down_idle': [], 'down_roll': [],
                           'left': [], 'left_attack': [], 'left_idle': [], 'left_roll': [],
                           'right': [], 'right_attack': [], 'right_idle': [], 'right_roll': [],
                           'up': [], 'up_attack': [], 'up_idle': [], 'up_roll': []}
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)

    def input(self) -> None:
        """Process keyboard inputs.
        """        
        keys = pygame.key.get_pressed()


        # make sure that if we're rolling we keep momentum, but when attacking we want to reset it
        if self.rolling:
            if self.direction.x == 0 and self.direction.y == 0:
                if "left" in self.status:
                    self.direction.x = -1
                elif "right" in self.status:
                    self.direction.x = 1
                elif "up" in self.status:
                    self.direction.y = -1
                elif "down" in self.status:
                    self.direction.y = 1
            return
        
        self.direction.x = 0
        self.direction.y = 0

        if self.attacking:
            return
        
        # Movement:
        if keys[pygame.K_UP]:
            self.direction.y -= 1
            self.status="up"
        if keys[pygame.K_DOWN]:
            self.direction.y += 1
            self.status="down"

        if keys[pygame.K_LEFT]:
            self.direction.x -= 1
            self.status="left"
        if keys[pygame.K_RIGHT]:
            self.direction.x += 1
            self.status="right"

        # Attack:
        if keys[pygame.K_f]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
        
        # Dodge roll:
        if keys[pygame.K_d] and not self.roll_used:
            self.rolling = True
            self.invulnerable = True
            self.roll_time = pygame.time.get_ticks()


    def get_status(self) -> None:
        """Changes the player status to reflect the current input
        """        
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status and not 'roll' in self.status:
                self.status += "_idle"
        
        if self.attacking:
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += "_attack"
        
        if self.rolling:
            if not 'roll' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_roll')
                else:
                    self.status += "_roll"


    def move(self, speed: Union[int, float]) -> None:
        """Process movement.

        Args:
            speed (Union[int, float]): Speed of the player.
        """        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if self.rolling:
            speed *= self.roll_speed_modifier
        
        if self.roll_used:
            speed *=self.post_roll_speed_modifier
        
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center


    def collision(self, direction: str) -> None:
        """Process and handle collisions.

        Args:
            direction (str): Either "horizontal" or "vertical" to process the directions individually.
        """        
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom


    def cooldowns(self) -> None:
        """Function that checks to see if the attack or roll cooldown has been completed
        """        
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_active:
                self.attacking = False
                self.status = self.status.replace('_attack', '')

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
            


    def animate(self) -> None:
        """Selects and displays the right frame of the current animation.
        """        
        animation = self.animations[self.status]
        
        # loop over frame index
        self.frame_index += PLAYER_ANIMATION_SPEED
        self.frame_index = self.frame_index % len(animation)
        
        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)


    def update(self) -> None:
        """Is run every frame, gets input and updates movement.
        """        
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)