import pygame
from typing import Union, Tuple, Dict

def basic_blit(destination: pygame.surface.Surface,
               source: pygame.surface.Surface,
               pos: Union[Tuple[int, int], pygame.Rect],
               area: Union[pygame.Rect, None] = None):
    """
    The basic blitting function to use. WE need to wrap this so we can support pre-multiplied alpha
    on post 2.0.0.dev10 versions of pygame and regular blitting on earlier versions.

    :param destination: Destination surface to blit on to.
    :param source: Source surface to blit from.
    :param pos: The position of our blit.
    :param area: The area of the source to blit from.

    """
    destination.blit(source, pos, area, special_flags=pygame.BLEND_ALPHA_SDL2)
    