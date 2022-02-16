from typing import Union, Tuple, Dict

import pygame
import pygame_gui

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core import UIElement
from pygame_gui.core.utility import render_white_text_alpha_black_bg, basic_blit, apply_colour_to_surface


class UIItem(UIElement):
    def __init__(self,
                 relative_rect: pygame.Rect,
                 image_surface: pygame.surface.Surface,
                 count: int,
                 manager: IUIManagerInterface,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent_element: UIElement = None,
                 object_id: Union[ObjectID, str, None] = None,
                 anchors: Dict[str, str] = None,
                 visible: int = 1):

        super().__init__(relative_rect, manager, container,
                         starting_height=1,
                         layer_thickness=1,

                         anchors=anchors,
                         visible=visible)

        self._create_valid_ids(container=container,
                               parent_element=parent_element,
                               object_id=object_id,
                               element_id='item')
        
        self.count = str(count)
        self.pic = image_surface

        self.font = None
        self.text_colour = None
        

        new_image = pygame.surface.Surface(self.relative_rect.size,
                                           flags=pygame.SRCALPHA,
                                           depth=32)
        new_image.fill(pygame.Color('#00000000'))
        
        self.item_img = pygame_gui.elements.UIImage(
            relative_rect,
            new_image,
            manager=manager,
            container=container
        )

        self.rebuild_from_changed_theme_data()        

        
    
    def rebuild_from_changed_theme_data(self):
        """
        Checks if any theming parameters have changed, and if so triggers a full rebuild of
        the element.

        """
        super().rebuild_from_changed_theme_data()
        any_changed = False

        font = self.ui_theme.get_font(self.combined_element_ids)
        if font != self.font:
            self.font = font
            any_changed = True    
            
        text_colour = self.ui_theme.get_colour_or_gradient('normal_text', self.combined_element_ids)
        if text_colour != self.text_colour:
            self.text_colour = text_colour
            any_changed = True
            
        if any_changed:
            self.rebuild()
        
    def kill(self):
        # self.item_count.kill()
        self.item_img.kill()
        return super().kill()

    def set_item(self, new_item_pic, new_item_count: int):
        self.count=str(new_item_count)
        self.pic=new_item_pic
        self.rebuild()
        

    def rebuild(self):
        new_image = pygame.surface.Surface(self.relative_rect.size,
                                           flags=pygame.SRCALPHA,
                                           depth=32)
        new_image.fill(pygame.Color('#00000000'))
        
        text_render = render_white_text_alpha_black_bg(self.font, self.count)
        apply_colour_to_surface(self.text_colour, text_render)
        
        text_render_rect = text_render.get_rect()
        pic_render_rect = self.get_relative_rect()
        
        basic_blit(new_image, pygame.transform.scale(self.pic, self.relative_rect.size), (0,0))
        
        
        basic_blit(new_image, text_render,  (pic_render_rect.w-text_render_rect.w, pic_render_rect.h-text_render_rect.h))

        self.item_img.set_image(new_image)
        
    

