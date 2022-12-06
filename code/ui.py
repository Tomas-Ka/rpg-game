import pygame
from settings import *
from player import Player


class UI:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, BAR_HEIGHT * 1.7, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # load all the weapon images into a list
        self.weapon_graphics = []
        for weapon in WEAPON_DATA.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(
            self,
            current: int,
            max_amount: int,
            bg_rect: pygame.Rect,
            colour: str) -> None:
        """Renders a bar onto the screen.

        Args:
            current (int): Current value of the bar.
            max_amount (int): Max value of the bar.
            bg_rect (pygame.Rect): The Rect object to modify and draw to screen.
            colour (str): pygame colour name or hex code
        """
        # draw background:
        pygame.draw.rect(self.display_surface, UI_BG_COLOUR, bg_rect)

        # stat -> ration conversion
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw bar:
        pygame.draw.rect(self.display_surface, colour, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 3)

    def show_exp(self, exp: int) -> None:
        """Renders exp amount onto the screen in the bottom right, on top of a background.

        Args:
            exp (int): Amount of Exp.
        """
        text_surf = self.font.render(str(exp), False, TEXT_COLOUR)
        x, y = self.display_surface.get_size()
        x, y = x - 20, y - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(
            self.display_surface,
            UI_BG_COLOUR,
            text_rect.inflate(
                20,
                20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface,
            UI_BORDER_COLOUR,
            text_rect.inflate(
                20,
                20),
            3)

    def selection_box(
            self,
            left: float,
            top: float,
            has_switched: bool) -> pygame.Rect:
        """Creates a box background at the given coords
        with an outline that turns gold if has switched is true.

        Args:
            left (float): Amount of pixels from the left side of the screen.
            top (float): Amount of pixels from the top of the screen.
            has_switched (bool): Whether or not to make the outline gold.

        Returns:
            pygame.Rect: The selection box object (not the outline)
        """
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOUR, bg_rect)
        if has_switched:
            pygame.draw.rect(
                self.display_surface,
                UI_BORDER_COLOUR_ACTIVE,
                bg_rect,
                3)
        else:
            pygame.draw.rect(
                self.display_surface,
                UI_BORDER_COLOUR,
                bg_rect,
                3)
        return bg_rect

    def weapon_overlay(self, weapon_index: int, has_switched: bool) -> None:
        """Creates a box in the bottom left corner containing the currently selected weapon.

        Args:
            weapon_index (int): Weapon index of player, what weapon they have equipped.
            has_switched (bool): If the player has recently switched weapons.
        """
        bg_rect = self.selection_box(10, self.display_surface.get_size()[
                                     1] - 10 - ITEM_BOX_SIZE, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player: Player) -> None:
        """Runs functions to blit all of the bars and other UI objects to the screen

        Args:
            player (Player): our player object
        """
        self.show_bar(
            player.health,
            player.stats['health'],
            self.health_bar_rect,
            HEALTH_COLOUR)
        self.show_bar(
            player.energy,
            player.stats['energy'],
            self.energy_bar_rect,
            ENERGY_COLOUR)

        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapons)
