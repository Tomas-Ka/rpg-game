import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import UI


class Level():
    def __init__(self) -> None:
        # get the display surface (the screen you can write to)
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprite
        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self) -> None:
        """Loads all the sprites of the game map into the group objects.
        """
        layout = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder("../graphics/grass"),
            'object': import_folder("../graphics/objects"),
        }
        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,
                                  y),
                                 [self.visible_sprites,
                                  self.obstacle_sprites],
                                 'grass',
                                 random_grass_image)
                        elif style == 'object':
                            object_sprite = graphics['object'][int(col)]
                            Tile(
                                (x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_sprite)

        self.player = Player((2000,
                              1400),
                             [self.visible_sprites],
                             self.obstacle_sprites,
                             self.create_attack,
                             self.destroy_attack)
        
        # Set camera position to player
        self.visible_sprites.camera_pos = pygame.math.Vector2(self.player.rect.center)

    def create_attack(self) -> None:
        """Creates a Weapon object and sets it as the current attack object.
        """
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self) -> None:
        """Destroyes the current attack object.
        """
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self) -> None:
        """Updates and draws all sprites.
        """
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.camera_pos = pygame.math.Vector2(0, 0)

        # creating the bg/floor
        self.floor_surface = pygame.image.load(
            '../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player: Player) -> None:
        """Customized draw function that y-sorts the sprites before writing them to the screen.
        This function also controlls the camera, and smoothly interpolates it towards the player.

        Args:
            player (Player): The player object for the game. Is used as the target for the camera.
        """
        # calculating new camera position
        heading = player.rect.center - self.camera_pos
        self.camera_pos += heading * SMOOTH_SPEED

        # getting offset
        self.offset.x = self.camera_pos.x - self.half_width
        self.offset.y = self.camera_pos.y - self.half_height

        # drawing floor
        offset_rect = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, offset_rect)

        # drawing sprites
        for sprite in sorted(self.sprites(),
                             key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)
