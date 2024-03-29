import pygame
from typing import Union
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, obstacle_sprites):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = PLAYER_ANIMATION_SPEED
        self.direction = pygame.math.Vector2()
        
        self.obstacle_sprites = obstacle_sprites
    
    def move(self, speed: Union[int, float]) -> None:
        """Process movement.

        Args:
            speed (Union[int, float]): Speed of the entity.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

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

    def animate(self) -> None:
        """Selects and displays the right frame of the current animation.
        """
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        self.frame_index = self.frame_index % len(animation)

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)