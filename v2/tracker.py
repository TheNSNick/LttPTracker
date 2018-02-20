import pygame
import sys
import os


TILE_SIZE = 32
MAP_SIZE = 276
LOCATION_SIZE = 10
LOCATION_BORDER = 2
SCREEN_WIDTH = 7 * TILE_SIZE + MAP_SIZE
SCREEN_HEIGHT = max(7 * TILE_SIZE, MAP_SIZE)
BG_COLOR = (0, 0, 0)
ALPHA_COLOR = (255, 0, 255)
BORDER_SELECTED_COLOR = (255, 255, 0)
LOCATION_AVAILABLE_COLOR = (0, 255, 0)
LOCATION_UNAVAILABLE_COLOR = (255, 0, 0)
MASKING_ALPHA = 128
FPS = 30
ITEM_COORDS = {'mail': (0, 0), 'sword': (1, 0), 'bow': (2, 0), 'boomerang': (3, 0), 'hookshot': (4, 0), 'mushroom': (5, 0), 'powder': (6, 0),
               'shield': (0, 1), 'moon_pearl': (1, 1), 'fire_rod': (2, 1), 'ice_rod': (3, 1), 'bombos': (4, 1), 'ether': (5, 1), 'quake': (6, 1),
               'ep': (0, 2), 'ep_chests': (1, 2), 'lantern': (2, 2), 'hammer': (3, 2), 'shovel': (4, 2), 'net': (5, 2), 'book': (6, 2),
               'dp': (0, 3), 'dp_chests': (1, 3), 'bottles': (2, 3), 'somaria': (3, 3), 'byrna': (4, 3), 'cape': (5, 3), 'mirror': (6, 3),
               'th': (0, 4), 'th_chests': (1, 4), 'boots': (2, 4), 'gloves': (3, 4), 'flippers': (4, 4), 'flute': (5, 4), 'aga': (6, 4),
               'pd': (0, 5), 'sp': (1, 5), 'sw': (2, 5), 'tt': (3, 5), 'ip': (4, 5), 'mm': (5, 5), 'tr': (6, 5),
               'pd_chests': (0, 6), 'sp_chests': (1, 6), 'sw_chests': (2, 6), 'tt_chests': (3, 6), 'ip_chests': (4, 6), 'mm_chests': (5, 6), 'tr_chests': (6, 6)
               }
ITEM_MAX = {'mail': 2, 'sword': 4, 'shield': 3, 'bow': 3, 'boomerang': 3, 'bottles': 4, 'gloves': 2,
            'ep_chests': 3, 'dp_chests': 2, 'th_chests': 2, 'pd_chests': 5, 'sp_chests': 6,
            'sw_chests': 2, 'tt_chests': 4, 'ip_chests': 3, 'mm_chests': 2, 'tr_chests': 5,
            'ep_crystal': 4, 'dp_crystal': 4, 'th_crystal': 4, 'pd_crystal': 4, 'sp_crystal': 4,
            'sw_crystal': 4, 'tt_crystal': 4, 'ip_crystal': 4, 'mm_crystal': 4, 'tr_crystal': 4,
            'mm_medallion': 3, 'tr_medallion': 3}
ITEM_UPGRADE = {'mail': 1, 'sword': 1, 'shield': 2, 'bow': 2, 'boomerang': 2, 'bottles': 1, 'gloves': 2, 'aga': 1}
BOSSES = {'ep': 'armos', 'dp': 'lanmola', 'th': 'moldorm', 'pd': 'helmasaur', 'sp': 'arrghus', 'sw': 'mothula', 'tt': 'blind', 'ip': 'kholdstare', 'mm': 'vitreous', 'tr': 'trinexx'}
CRYSTALS = {1: 'green_pendant', 2: 'other_pendant', 3: 'blue_crystal', 4: 'red_crystal'}
MEDALLIONS = {1: 'bombos', 2: 'ether', 3: 'quake'}
LIGHT_WORLD_COORDS = {'links_house': (152, 192), 'escape_front': (136, 121), 'escape_dark': (136, 106),
                      'escape_back': (136, 90), 'uncle_tunnel': (154, 123), 'lumberjack_cave': (85, 30),
                      'lost_woods_ledge': (52, 49), 'mushroom_spot': (36, 36), 'pedestal': (20, 20),
                      'kakariko_well': (14, 120), 'blinds_house': (38, 120), 'bottle_vendor': (31, 135),
                      'chicken_house':(32, 155), 'sick_kid': (52, 148), 'tavern': (52, 162), 'blacksmiths': (85, 148),
                      'magic_bat': (100, 156), 'library': (54, 184), 'hedge_race': (22, 180), 'grove_dig': (85, 180),
                      'grove_ledge': (69, 207), 'desert_ledge': (10, 236), 'checkerboard_cave': (55, 218),
                      'aginahs_cave': (68, 234), 'bombos_tablet': (65, 255), 'purple_chest': (99, 242),
                      'dam': (130, 258), 'mini_moldorm_cave': (178, 250), 'ice_rod_cave': (247, 209),
                      'hylia_island': (194, 228), 'hobo': (193, 196), 'witchs_hut': (215, 95),
                      'waterfall_fairy': (238, 60), 'king_zora': (261, 45), 'zora_ledge': (257, 58),
                      'old_man': (112, 60), 'spectacle_rock': (138, 33), 'spectacle_cave': (126, 44),
                      'ether_tablet': (126, 20), 'paradox_cave': (220, 66), 'spiral_cave': (202, 36),
                      'mimic_cave': (214, 52), 'floating_island': (210, 10), 'bonk_rocks': (105, 85),
                      'sanctuary': (120, 87), 'kings_tomb': (162, 93), 'graveyard_ledge': (150, 85),
                      'sashas_hut': (214, 116), 'sasha': (214, 130)
                      }


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    items = load_items()
    item_bg_image = pygame.image.load(os.path.join('gfx', 'item_bg.png')).convert()
    item_bg_image.set_colorkey(ALPHA_COLOR)
    light_world_bg_image = pygame.image.load(os.path.join('gfx', 'light_world_map.png')).convert()
    mouse_coords = (0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                mouse_coords = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_handler(event.button, event.pos, items)
        screen.fill(BG_COLOR)
        item_image = compose_item_image(item_bg_image, items)
        light_world_image = compose_light_world_image(light_world_bg_image, items, mouse_coords)
        screen.blit(item_image, (0, 0))
        screen.blit(light_world_image, (7 * TILE_SIZE, 0))
        pygame.display.update()
        clock.tick(FPS)


def load_items():
    items = dict()
    for item_name in ITEM_COORDS.keys():
        items[item_name] = 0
        if item_name in BOSSES.keys():
            items['{}_crystal'.format(item_name)] = 0
            if item_name in ['mm', 'tr']:
                items['{}_medallion'.format(item_name)] = 0
    return items


def apply_alpha_and_blit(draw_surface, image_path, draw_coordinates=(0, 0)):
    draw_image = pygame.image.load(image_path).convert()
    draw_image.set_colorkey(ALPHA_COLOR)
    draw_surface.blit(draw_image, draw_coordinates)


def compose_item_image(bg_image, item_dict):
    working_image = pygame.Surface((bg_image.get_width(), bg_image.get_height()))
    bg_image.set_colorkey(ALPHA_COLOR)
    working_image.blit(bg_image, (0, 0))
    masking_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    masking_image.fill(BG_COLOR)
    masking_image.set_alpha(MASKING_ALPHA)
    blanking_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    blanking_image.fill(BG_COLOR)
    for item_name, coords in ITEM_COORDS.iteritems():
        screen_coords = coords[0] * TILE_SIZE, coords[1] * TILE_SIZE
        # masking
        if item_dict[item_name] == 0 and 'chests' not in item_name and item_name not in ['mail', 'aga']:
            working_image.blit(masking_image, screen_coords)
        # upgrades / crystals / medallions
        if item_dict[item_name] > 0:
            # chest upgrades
            if 'chests' in item_name:
                chest_path = os.path.join('gfx', 'chest_{}_{}.png'.format(ITEM_MAX[item_name], item_dict[item_name]))
                apply_alpha_and_blit(working_image, chest_path, screen_coords)
            # item upgrades
            elif item_name in ITEM_UPGRADE.keys() and item_dict[item_name] >= ITEM_UPGRADE[item_name]:
                working_image.blit(blanking_image, screen_coords)
                item_path = os.path.join('gfx', '{}_{}.png'.format(item_name, item_dict[item_name]))
                apply_alpha_and_blit(working_image, item_path, screen_coords)
        # crystals
        if item_name in BOSSES.keys() and item_dict['{}_crystal'.format(item_name)] > 0:
            crystal_coords = screen_coords[0], screen_coords[1] + TILE_SIZE / 2
            crystal_path = os.path.join('gfx', '{}.png'.format(CRYSTALS[item_dict['{}_crystal'.format(item_name)]]))
            apply_alpha_and_blit(working_image, crystal_path, crystal_coords)
        # medallions
        if item_name in ['mm', 'tr'] and item_dict['{}_medallion'.format(item_name)] > 0:
            medallion_coords = screen_coords[0] + TILE_SIZE / 2, screen_coords[1] + TILE_SIZE / 2
            medallion_path = os.path.join('gfx', '{}_small.png'.format(MEDALLIONS[item_dict['{}_medallion'.format(item_name)]]))
            apply_alpha_and_blit(working_image, medallion_path, medallion_coords)
    return working_image


def click_handler(click_button, click_coords, item_dict):
    click_coords_scaled = click_coords[0] / TILE_SIZE, click_coords[1] / TILE_SIZE
    if max(click_coords_scaled) < 7:
        for item_name, item_coords in ITEM_COORDS.iteritems():
            if item_coords == click_coords_scaled:
                adjust_name = item_name
                if item_name in BOSSES.keys() and click_coords[1] % TILE_SIZE > TILE_SIZE / 2:
                    if click_coords[0] % TILE_SIZE < TILE_SIZE / 2:
                        adjust_name += '_crystal'
                    elif item_name in ['mm', 'tr']:
                        adjust_name += '_medallion'
                if click_button == 1:
                    item_dict[adjust_name] += 1
                    if item_dict[adjust_name] > ITEM_MAX.get(adjust_name, 1):
                        item_dict[adjust_name] = 0
                    break
                elif click_button == 3:
                    item_dict[adjust_name] -= 1
                    if item_dict[adjust_name] < 0:
                        item_dict[adjust_name] = ITEM_MAX.get(adjust_name, 1)
                    break


def dark_world_access(items):
    dw_points = dict()
    dw_points['castle'] = bool(items['aga'])
    dw_points['lost_woods'] = items['gloves'] >= 2 or (bool(items['hammer']) and bool(items)['gloves'])
    dw_points['east'] = (bool(items['gloves']) and bool(items['hammer'])) or items['gloves'] >= 2
    dw_points['swamp'] = dw_points['east']
    dw_points['lake'] = bool(items['flippers']) and items['gloves'] >= 2
    dw_points['desert'] = bool(items['flute']) and items['gloves'] >= 2
    dw_points['dm_west'] = bool(items['flute']) or (bool(items['gloves']) and bool(items['lantern']))
    dw_points['dm_east'] = dw_points['dm_west'] and items['gloves'] >= 2 and (bool(items['hookshot']) \
                            or (bool(items['mirror']) and bool(items['hammer'])))
    dw_points['t_rock'] = dw_points['dm_west'] and bool(items['hammer']) and items['gloves'] >= 2 \
                            and (bool(items['hookshot']) or (bool(items['mirror']) and bool(items['hammer'])))
    return dw_points


def pendants(items):
    green = 0
    other = 0
    red = 0
    for item_name, amount in items.iteritems():
        if 'crystal' in item_name and amount > 0:
            crystal_dungeon = item_name[:2]
            if items[crystal_dungeon]:
                if amount == 1:
                    green += 1
                elif amount == 2:
                    other += 1
                elif amount == 4:
                    red += 1
    return green, other, red


def light_world_availability(items):
    dw_spots = dark_world_access(items)
    green_pendant, other_pendants, red_crystals = pendants(items)
    lw_locs = dict()
    lw_locs['links_house'] = True
    lw_locs['uncle_tunnel'] = True
    lw_locs['escape_front'] = True
    lw_locs['escape_dark'] = bool(items['lantern'])
    lw_locs['escape_back'] = bool(items['lantern']) or bool(items['gloves'])
    lw_locs['lumberjack_cave'] = bool(items['aga'])
    lw_locs['lost_woods_ledge'] = True
    lw_locs['mushroom_spot'] = True
    lw_locs['pedestal'] = bool(green_pendant) and other_pendants >= 2
    lw_locs['kakariko_well'] = True
    lw_locs['blinds_house'] = True
    lw_locs['bottle_vendor'] = True
    lw_locs['chicken_house'] = True
    lw_locs['sick_kid'] = bool(items['bottles'])
    lw_locs['tavern'] = True
    lw_locs['blacksmiths'] = items['gloves'] >= 2
    lw_locs['magic_bat'] = bool(items['powder'])
    lw_locs['library'] = bool(items['boots'])
    lw_locs['hedge_race'] = True
    lw_locs['grove_dig'] = bool(items['shovel'])
    lw_locs['grove_ledge'] = bool(items['mirror']) and \
        (dw_spots['lost_woods'] or dw_spots['swamp'] or (dw_spots['castle'] and (items['hammer'] or items['hookshot'])))
    lw_locs['desert_ledge'] = bool(items['book']) or (dw_spots['desert'] and bool(items['mirror']))
    lw_locs['checkerboard_cave'] = lw_locs['desert_ledge'] and bool(items['mirror'])
    lw_locs['aginahs_cave'] = True
    lw_locs['bombos_tablet'] = bool(items['mirror']) and items['sword'] >= 2 and \
        (dw_spots['lost_woods'] or dw_spots['swamp'] or (dw_spots['castle'] and (items['hammer'] or items['hookshot'])))
    lw_locs['purple_chest'] = items['gloves'] >= 2
    lw_locs['dam'] = True
    lw_locs['mini_moldorm_cave'] = True
    lw_locs['ice_rod_cave'] = True
    lw_locs['hylia_island'] = bool(items['flippers']) and bool(items['mirror']) and \
        (dw_spots['lost_woods'] or dw_spots['swamp'] or (dw_spots['castle'] and (items['hammer'] or items['hookshot'])))
    lw_locs['hobo'] = bool(items['flippers'])
    lw_locs['witchs_hut'] = bool(items['mushroom'])
    lw_locs['waterfall_fairy'] = bool(items['flippers']) and bool(items['gloves'])
    lw_locs['king_zora'] = bool(items['gloves'])
    lw_locs['zora_ledge'] = bool(items['flippers']) and bool(items['gloves'])
    lw_locs['old_man'] = bool(items['lantern']) and (bool(items['gloves']) or bool(items['flute']))
    lw_locs['spectacle_rock'] = dw_spots['dm_west']
    lw_locs['spectacle_cave'] = dw_spots['dm_west']
    lw_locs['ether_tablet'] = bool(items['book']) and items['sword'] >= 2 and dw_spots['dm_west'] and \
                              (bool(items['mirror']) or (bool(items['hookshot']) and bool(items['hammer'])))
    lw_locs['paradox_cave'] = dw_spots['dm_west'] and \
                              (bool(items['hookshot']) or (bool(items['mirror'])) and bool(items['hammer']))
    lw_locs['spiral_cave'] = lw_locs['paradox_cave']
    lw_locs['mimic_cave'] = dw_spots['t_rock'] and bool(items['tr_medallion']) \
                            and bool(items['cane_somaria']) and bool(items['mirror'])
    lw_locs['floating_island'] = bool(items['mirror']) # ...and... TODO
    lw_locs['bonk_rocks'] = bool(items['boots'])
    lw_locs['kings_tomb'] = bool(items['boots']) and (items['gloves'] >= 2 or (bool(items['mirror']) and \
                                            (dw_spots['lost_woods'] or (dw_spots['castle'] and \
                                            (bool(items['hookshot']) or bool(items['hammer']))) or dw_spots['swamp'])))
    lw_locs['graveyard_ledge'] = bool(items['mirror']) and \
                                            (dw_spots['lost_woods'] or (dw_spots['castle'] and \
                                            (bool(items['hookshot']) or bool(items['hookshot']))) or dw_spots['swamp'])
    lw_locs['sashas_hut'] = True
    lw_locs['sasha'] = bool(green_pendant)
    return lw_locs


def compose_light_world_image(bg_image, item_dict, mouse_coords):
    working_image = pygame.Surface((bg_image.get_width(), bg_image.get_height()))
    working_image.blit(bg_image, (0, 0))
    locations = light_world_availability(item_dict)
    pointer_coords = mouse_coords[0] - TILE_SIZE * 7, mouse_coords[1]
    for location_name, availability in locations.iteritems():
        # border
        location_coords = LIGHT_WORLD_COORDS[location_name]
        border_coords = location_coords[0] - LOCATION_BORDER, location_coords[1] - LOCATION_BORDER
        border_size = LOCATION_SIZE + 2 * LOCATION_BORDER
        border_rect = pygame.Rect(border_coords, (border_size, border_size))
        border_color = BG_COLOR
        if border_rect.collidepoint(pointer_coords[0], pointer_coords[1]):
            border_color = BORDER_SELECTED_COLOR
        pygame.draw.rect(working_image, border_color, border_rect)
        # inner rect ( TODO -- checked items should be grey )
        location_rect = pygame.Rect(location_coords, (LOCATION_SIZE, LOCATION_SIZE))
        location_color = LOCATION_UNAVAILABLE_COLOR
        if locations[location_name]:
            location_color = LOCATION_AVAILABLE_COLOR
        pygame.draw.rect(working_image, location_color, location_rect)
    # TODO -- dungeons
    return working_image


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
