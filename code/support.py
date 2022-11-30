from csv import reader
from os import walk
import pygame
from typing import List

def import_csv_layout(path: str) -> List[List[int]]:
    """Imports a csv and parses it to a 2d array.

    Args:
        path (str): Path to the csv file.

    Returns:
        List[List[int]]: a 2d array containing the level data of the csv
    """
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(row)
        return terrain_map


def import_folder(path: str) -> List[pygame.Surface]:
    """Returns all images in a folder parsed as pygame surfaces.

    Args:
        path (str): Path to the folder.

    Returns:
        List[pygame.Surface]: An array containing the parsed surfaces.
    """ 
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = f"{path}/{image}"
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list