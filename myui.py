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
        self.pic_size = relative_rect.size

        self.font = None
        self.text_colour = None

        self.relative_rect.size = (0,0)
        new_image = pygame.surface.Surface((self.relative_rect.size),
                                           flags=pygame.SRCALPHA,
                                           depth=32)
        new_image.fill(pygame.Color('#00000000'))
        
        self.item_img = pygame_gui.elements.UIImage(
            self.relative_rect,
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
            
        pic_size = self.ui_theme.get_misc_data('size', self.combined_element_ids)
        if pic_size != self.pic_size and (self.pic_size[0]==-1 or self.pic_size[1]==-1):
            self.pic_size = (int(pic_size), int(pic_size))
            self.relative_rect.size = self.pic_size
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
        

class UIItemsList(UIElement):
    
        # itemsui= UIItemsList(
        #     relative_rect=items_rect,
        #     items_list=items_list,
        #     manager=self.app.manager,
        #     container=self.panel_info,
        #     object_id='item_label_m'
        # )    
    
    def __init__(self,
                 relative_rect: pygame.Rect,
                 items_list,
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
                               element_id='items_list')
        
        self.items_list = items_list
        self.pic_size = (relative_rect.height, relative_rect.height)

        self.font = None
        self.text_colour = None
        self.padding = (5, 5)

        self.relative_rect.size = (0,0)
        
        self.item_img_list = []
        for item in self.items_list:
            new_image = pygame.surface.Surface((self.relative_rect.size),
                                            flags=pygame.SRCALPHA,
                                            depth=32)
            new_image.fill(pygame.Color('#00000000'))
            
            item_img = pygame_gui.elements.UIImage(
                self.relative_rect,
                new_image,
                manager=manager,
                container=container
            )
            self.item_img_list.append((item_img, item['img'], item['count']))

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
            
        pic_size = self.ui_theme.get_misc_data('size', self.combined_element_ids)
        if pic_size != self.pic_size and (self.pic_size[0]==-1 or self.pic_size[1]==-1):
            self.pic_size = (int(pic_size)-self.padding[0]*2, int(pic_size)-self.padding[1]*2)
            any_changed = True
        
        def tuple_extract(str_data: str) -> Tuple[int, int]:
            return int(str_data.split(',')[0]), int(str_data.split(',')[1])

        if self._check_misc_theme_data_changed(attribute_name='padding',
                                               default_value=(5, 5),
                                               casting_func=tuple_extract):
            self.pic_size = (int(pic_size)-self.padding[0]*2, int(pic_size)-self.padding[1]*2)
            any_changed = True        
        
        if any_changed:
            self.rebuild()
        
    def kill(self):
        # self.item_count.kill()
        for item in self.item_img_list:
            item[0].kill()
            del item
        self.items_list.clear()
            
        return super().kill()

    def set_items_list(self, new_item_list):
        if new_item_list!=self.items_list:
            self.items_list=new_item_list
            self.rebuild()
        

    def rebuild(self):
        left = 0
        self.relative_rect.size = (len(self.item_img_list)*(self.pic_size[0]+self.padding[0]), self.pic_size[1]+self.padding[1])
        for item in self.item_img_list:
            newpos = (left, item[0].relative_rect.top)
            item[0].relative_rect.size = (self.pic_size[0]+self.padding[0]*2, self.pic_size[1]+self.padding[1]*2)
            item[0].set_relative_position(newpos)
            left += self.pic_size[0]+self.padding[0]
        
        
            new_image = pygame.surface.Surface(item[0].relative_rect.size,
                                            flags=pygame.SRCALPHA,
                                            depth=32)
            new_image.fill(pygame.Color('#00000000'))
        
            text_render = render_white_text_alpha_black_bg(self.font, str(item[2]))
            apply_colour_to_surface(self.text_colour, text_render)
        
            text_render_rect = text_render.get_rect()
            pic_render_rect = item[0].get_relative_rect()
            
        
            basic_blit(new_image, pygame.transform.scale(item[1], self.pic_size), (self.padding[0],self.padding[1]))
            basic_blit(new_image, text_render,  (pic_render_rect.w-text_render_rect.w-self.padding[0], pic_render_rect.h-text_render_rect.h-self.padding[1]))

            item[0].set_image(new_image)
            

    

