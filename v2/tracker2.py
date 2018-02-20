import pygame
import sys
import os

TILE_SIZE = 32
MAP_SIZE = 276
ITEM_IMAGE_COORDS = (0, 0)
LIGHT_WORLD_IMAGE_COORDS = (7 * TILE_SIZE, 0)
DARK_WORLD_IMAGE_COORDS = (7 * TILE_SIZE + MAP_SIZE, 0)
LOCATION_SIZE = 9
LOCATION_BORDER = 2
DUNGEON_SIZE = 24
DUNGEON_INNER_SIZE = 16
DUNGEON_BORDER = 3
SCREEN_WIDTH = 7 * TILE_SIZE + 2 * MAP_SIZE
SCREEN_HEIGHT = max(7 * TILE_SIZE, MAP_SIZE)
BG_COLOR = (0, 0, 0)
ALPHA_COLOR = (255, 0, 255)
BORDER_SELECTED_COLOR = (255, 255, 0)
LOCATION_AVAILABLE_COLOR = (0, 255, 0)
LOCATION_UNAVAILABLE_COLOR = (255, 0, 0)
LOCATION_CHECKED_COLOR = (128, 128, 128)
MASKING_ALPHA = 128
FPS = 30
ITEM_COORDS = {
    (0, 0): 'mail', (1, 0): 'sword', (2, 0): 'bow', (3, 0): 'boomerang', (4, 0): 'hookshot', (5, 0): 'mushroom', (6, 0): 'powder',
    (0, 1): 'shield', (1, 1): 'moon_pearl', (2, 1): 'fire_rod', (3, 1): 'ice_rod', (4, 1): 'bombos', (5, 1): 'ether', (6, 1): 'quake',
    (0, 2): 'ep', (1, 2): 'ep_chests', (2, 2): 'lantern', (3, 2): 'hammer', (4, 2): 'shovel', (5, 2): 'net', (6, 2): 'book',
    (0, 3): 'dp', (1, 3): 'dp_chests', (2, 3): 'bottles', (3, 3): 'somaria', (4, 3): 'byrna', (5, 3): 'cape', (6, 3): 'mirror',
    (0, 4): 'th', (1, 4): 'th_chests', (2, 4): 'boots', (3, 4): 'gloves', (4, 4): 'flippers', (5, 4): 'flute', (6, 4): 'aga',
    (0, 5): 'pd', (1, 5): 'sp', (2, 5): 'sw', (3, 5): 'tt', (4, 5): 'ip', (5, 5): 'mm', (6, 5): 'tr',
    (0, 6): 'pd_chests', (1, 6): 'sp_chests', (2, 6): 'sw_chests', (3, 6): 'tt_chests', (4, 6): 'ip_chests', (5, 6): 'mm_chests', (6, 6): 'tr_chests'
               }
ITEM_MAX = {'mail': 2, 'sword': 4, 'shield': 3, 'bow': 3, 'boomerang': 3, 'bottles': 4, 'gloves': 2,
            'ep_chests': 3, 'dp_chests': 2, 'th_chests': 2, 'pd_chests': 5, 'sp_chests': 6,
            'sw_chests': 2, 'tt_chests': 4, 'ip_chests': 3, 'mm_chests': 2, 'tr_chests': 5,
            'ep_crystal': 4, 'dp_crystal': 4, 'th_crystal': 4, 'pd_crystal': 4, 'sp_crystal': 4,
            'sw_crystal': 4, 'tt_crystal': 4, 'ip_crystal': 4, 'mm_crystal': 4, 'tr_crystal': 4,
            'mm_medallion': 3, 'tr_medallion': 3}
ITEM_UPGRADE = {'mail': 1, 'sword': 1, 'shield': 2, 'bow': 2, 'boomerang': 2, 'bottles': 1, 'gloves': 2, 'aga': 1}
CRYSTALS = {1: 'green_pendant', 2: 'other_pendant', 3: 'blue_crystal', 4: 'red_crystal'}
MEDALLIONS = {1: 'bombos', 2: 'ether', 3: 'quake'}
LIGHT_WORLD_COORDS = {'links_house': (155, 195), 'escape_front': (143, 126), 'escape_dark': (143, 112),
                      'escape_back': (143, 99), 'uncle_tunnel': (156, 125), 'lumberjack_cave': (91, 36),
                      'lost_woods_ledge': (55, 50), 'mushroom_spot': (37, 43), 'pedestal': (24, 26),
                      'kakariko_well': (23, 127), 'blinds_house': (43, 124), 'bottle_vendor': (35, 139),
                      'chicken_house':(39, 155), 'sick_kid': (55, 151), 'tavern': (55, 164), 'blacksmiths': (95, 155),
                      'magic_bat': (100, 165), 'library': (59, 188), 'hedge_race': (27, 188), 'grove_dig': (89, 185),
                      'grove_ledge': (71, 212), 'desert_ledge': (14, 245), 'checkerboard_cave': (57, 225),
                      'aginahs_cave': (72, 236), 'bombos_tablet': (79, 255), 'purple_chest': (103, 249),
                      'dam': (133, 259), 'mini_moldorm_cave': (183, 253), 'ice_rod_cave': (252, 211),
                      'hylia_island': (199, 230), 'hobo': (195, 197), 'witchs_hut': (219, 99),
                      'waterfall_fairy': (248, 67), 'king_zora': (261, 51), 'zora_ledge': (262, 63),
                      'old_man': (115, 62), 'spectacle_rock': (144, 37), 'spectacle_cave': (139, 50),
                      'ether_tablet': (130, 25), 'paradox_cave': (224, 70), 'spiral_cave': (206, 40),
                      'mimic_cave': (218, 56), 'floating_island': (214, 14), 'bonk_rocks': (109, 89),
                      'kings_tomb': (166, 97), 'graveyard_ledge': (154, 89), 'sashas_hut': (218, 120),
                      'sasha': (218, 134), 'sanctuary': (131, 88)
                      }
LIGHT_WORLD_DUNGEON_COORDS = {'ep': (248, 124), 'dp': (32, 220), 'th': (164, 16)}
DARK_WORLD_COORDS = {'chest_game': (25, 137), 'c_house': (65, 137), 'bomb_hut': (41, 168), 'peg_cave': (94, 165),
                     'dig_game': (27, 188), 'flute_kid': (94, 190), 'mire_shed': (21, 218), 'hype_cave': (166, 219),
                     'pyramid': (165, 120), 'pyramid_fairy': (134, 138), 'catfish': (250, 60), 'bumper_cave': (98, 52),
                     'spike_cave': (147, 45), 'hookshot_cave_bottom': (213, 41), 'hookshot_cave_full': (211, 30),
                     'super_bunny_cave': (226, 61)}
DARK_WORLD_DUNGEON_COORDS = {'pd': (230, 144), 'sp': (132, 256), 'sw': (33, 33), 'tt': (45, 142),
                             'ip': (216, 238), 'mm': (40, 242), 'tr': (258, 28)}


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    items = load_items()
    selected_location = None
    checked_locations = []
    item_bg_image = pygame.image.load(os.path.join('gfx', 'item_bg.png')).convert()
    light_world_bg_image = pygame.image.load(os.path.join('gfx', 'light_world_map.png')).convert()
    dark_world_bg_image = pygame.image.load(os.path.join('gfx', 'dark_world_map.png')).convert()
    while True:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                selected_location = location_at_coords(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in [1, 3]:
                if selected_location:
                    if selected_location in checked_locations:
                        checked_locations.remove(selected_location)
                    else:
                        checked_locations.append(selected_location)
                elif item_scaled_coords(event.pos):
                    item_click(event.pos, event.button, items)
        # draw/tick
        screen.fill(BG_COLOR)
        item_image = compose_item_image(item_bg_image, items)
        screen.blit(item_image, ITEM_IMAGE_COORDS)
        light_world_image = compose_light_world_image(light_world_bg_image, items, selected_location, checked_locations)
        screen.blit(light_world_image, LIGHT_WORLD_IMAGE_COORDS)
        dark_world_image = compose_dark_world_image(dark_world_bg_image, items, selected_location, checked_locations)
        screen.blit(dark_world_image, DARK_WORLD_IMAGE_COORDS)
        pygame.display.update()
        clock.tick(FPS)


def load_items():
    items = {}
    item_names = list(set(ITEM_COORDS.values() + ITEM_MAX.keys()))
    for item_name in item_names:
        items[item_name] = 0
    return items


def light_world_location_rects():
    rects = {}
    rect_size = LOCATION_SIZE + 2 * LOCATION_BORDER
    for location_name, location_coords in LIGHT_WORLD_COORDS.iteritems():
        location_rect = pygame.Rect(0, 0, rect_size, rect_size)
        location_rect.center = location_coords
        rects[location_name] = location_rect
    return rects


def light_world_dungeon_rects():
    rects = dict()
    rect_size = DUNGEON_SIZE + 2 * DUNGEON_BORDER
    for dungeon_name, dungeon_coords in LIGHT_WORLD_DUNGEON_COORDS.iteritems():
        dungeon_rect = pygame.Rect(0, 0, rect_size, rect_size)
        dungeon_rect.center = dungeon_coords
        rects[dungeon_name] = dungeon_rect
    return rects


def dark_world_rects():
    rects = {}
    rect_size = LOCATION_SIZE + 2 * LOCATION_BORDER
    for location_name, location_coords in DARK_WORLD_COORDS.iteritems():
        location_rect = pygame.Rect(0, 0, rect_size, rect_size)
        location_rect.center = location_coords
        rects[location_name] = location_rect
    return rects


def dark_world_dungeon_rects():
    rects = dict()
    rect_size = DUNGEON_SIZE + 2 * DUNGEON_BORDER
    for dungeon_name, dungeon_coords in DARK_WORLD_DUNGEON_COORDS.iteritems():
        dungeon_rect = pygame.Rect(0, 0, rect_size, rect_size)
        dungeon_rect.center = dungeon_coords
        rects[dungeon_name] = dungeon_rect
    return rects


def location_at_coords(coords):
    # check light world
    check_coords = coords[0] - LIGHT_WORLD_IMAGE_COORDS[0], coords[1] - LIGHT_WORLD_IMAGE_COORDS[1]
    location_rects = light_world_location_rects()
    for location_name, location_rect in location_rects.iteritems():
        if location_rect.collidepoint(check_coords):
            return location_name
    dungeon_rects = light_world_dungeon_rects()
    for dungeon_name, dungeon_rect in dungeon_rects.iteritems():
        if dungeon_rect.collidepoint(check_coords):
            return dungeon_name
    # check dark world
    check_coords = coords[0] - DARK_WORLD_IMAGE_COORDS[0], coords[1] - DARK_WORLD_IMAGE_COORDS[1]
    location_rects = dark_world_rects()
    for location_name, location_rect in location_rects.iteritems():
        if location_rect.collidepoint(check_coords):
            return location_name
    dungeon_rects = dark_world_dungeon_rects()
    for dungeon_name, dungeon_rect in dungeon_rects.iteritems():
        if dungeon_rect.collidepoint(check_coords):
            return dungeon_name
    return None


def item_scaled_coords(coords):
    if max(coords[0] / TILE_SIZE, coords[1] / TILE_SIZE) < 7:
        return coords[0] / TILE_SIZE, coords[1] / TILE_SIZE
    return None


def item_click(click_coords, click_button, item_dict):
    item_name = ITEM_COORDS[item_scaled_coords(click_coords)]
    if len(item_name) == 2 and click_coords[1] % TILE_SIZE > TILE_SIZE / 2:
        if click_coords[0] % TILE_SIZE <= TILE_SIZE / 2:
            item_name += '_crystal'
        elif item_name in ['mm', 'tr']:
            item_name += '_medallion'
    if click_button == 1:
        item_dict[item_name] += 1
        if item_dict[item_name] > ITEM_MAX.get(item_name, 1):
            item_dict[item_name] = 0
    elif click_button == 3:
        item_dict[item_name] -= 1
        if item_dict[item_name] < 0:
            item_dict[item_name] = ITEM_MAX.get(item_name, 1)


def apply_alpha_and_blit(draw_surface, image_path, draw_coordinates=(0, 0)):
    draw_image = pygame.image.load(image_path).convert()
    draw_image.set_colorkey(ALPHA_COLOR)
    draw_surface.blit(draw_image, draw_coordinates)


def compose_item_image(item_bg, item_dict):
    working_image = pygame.Surface((7 * TILE_SIZE, 7 * TILE_SIZE))
    working_image.set_colorkey(ALPHA_COLOR)
    item_bg.set_colorkey(ALPHA_COLOR)
    working_image.blit(item_bg, (0, 0))
    masking_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    masking_image.fill(BG_COLOR)
    masking_image.set_alpha(MASKING_ALPHA)
    blanking_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    blanking_image.fill(BG_COLOR)
    for coords, item_name in ITEM_COORDS.iteritems():
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
        if len(item_name) == 2 and item_dict['{}_crystal'.format(item_name)] > 0:
            crystal_coords = screen_coords[0], screen_coords[1] + TILE_SIZE / 2
            crystal_path = os.path.join('gfx', '{}.png'.format(CRYSTALS[item_dict['{}_crystal'.format(item_name)]]))
            apply_alpha_and_blit(working_image, crystal_path, crystal_coords)
        # medallions
        if item_name in ['mm', 'tr'] and item_dict['{}_medallion'.format(item_name)] > 0:
            medallion_coords = screen_coords[0] + TILE_SIZE / 2, screen_coords[1] + TILE_SIZE / 2
            medallion_path = os.path.join('gfx', '{}_small.png'.format(MEDALLIONS[item_dict['{}_medallion'.format(item_name)]]))
            apply_alpha_and_blit(working_image, medallion_path, medallion_coords)
    return working_image


def pendants(item_dict):
    green = 0
    other = 0
    red = 0
    for item_name, amount in item_dict.iteritems():
        if 'crystal' in item_name and amount > 0:
            crystal_dungeon = item_name[:2]
            if item_dict[crystal_dungeon]:
                if amount == 1:
                    green += 1
                elif amount == 2:
                    other += 1
                elif amount == 4:
                    red += 1
    return green, other, red


def dungeon_medallions(item_dict):
    medallion_dict = {'mm': False, 'tr': False}
    for dungeon in medallion_dict.keys():
        if bool(item_dict['{}_medallion'.format(dungeon)]):
            medallion_name = MEDALLIONS[item_dict['{}_medallion'.format(dungeon)]]
            if bool(item_dict[medallion_name]):
                medallion_dict[dungeon] = True
    return medallion_dict


def dark_world_areas(item_dict):
    locs = dict()
    locs['north'] = item_dict['gloves'] >= 2 or (bool(item_dict['hammer']) and bool(item_dict['gloves'])) or \
                    (item_dict['aga'] and (bool(item_dict['hammer']) or bool(item_dict['gloves'])) and
                     bool(item_dict['hookshot']))
    locs['south'] = (bool(item_dict['hammer']) and bool(item_dict['gloves'])) or locs['north'] or \
                    (item_dict['aga'] and item_dict['hammer'])
    locs['east'] = item_dict['aga'] or (item_dict['gloves'] and item_dict['hammer']) or \
                   (locs['south'] and item_dict['flippers'])
    locs['mire'] = bool(item_dict['flute']) and item_dict['gloves'] >= 2
    locs['ice'] = bool(item_dict['flippers']) and item_dict['gloves'] >= 2
    locs['dm_west'] = bool(item_dict['flute']) or (bool(item_dict['lantern']) and bool(item_dict['gloves']))
    locs['dm_east'] = locs['dm_west'] and item_dict['gloves'] >= 2 and \
                      (item_dict['hookshot'] or (item_dict['mirror'] and item_dict['hammer']))
    return locs


def light_world_availability(item_dict):
    green_pendant, other_pendants, _ = pendants(item_dict)
    medals = dungeon_medallions(item_dict)
    dw_access = dark_world_areas(item_dict)
    locs = dict()
    locs['escape_dark'] = bool(item_dict['lantern'])
    locs['escape_back'] = bool(item_dict['lantern']) or bool(item_dict['gloves'])
    locs['lumberjack_cave'] = bool(item_dict['aga']) and bool(item_dict['boots'])
    locs['pedestal'] = bool(green_pendant) and other_pendants >= 2
    locs['sick_kid'] = bool(item_dict['bottles'])
    locs['blacksmiths'] = item_dict['gloves'] >= 2
    locs['magic_bat'] = bool(item_dict['powder'])
    locs['library'] = bool(item_dict['boots'])
    locs['grove_dig'] = bool(item_dict['shovel'])
    locs['grove_ledge'] = bool(item_dict['mirror']) and dw_access['south']
    locs['desert_ledge'] = bool(item_dict['book']) or (dw_access['mire'] and bool(item_dict['mirror']))
    locs['checkerboard_cave'] = dw_access['mire'] and bool(item_dict['mirror'])
    locs['bombos_tablet'] = bool(item_dict['book']) and item_dict['sword'] >= 2 and \
                            bool(item_dict['mirror']) and dw_access['south']
    locs['purple_chest'] = item_dict['gloves'] >= 2
    locs['hylia_island'] = bool(item_dict['flippers']) and bool(item_dict['mirror']) and dw_access['south']
    locs['hobo'] = bool(item_dict['flippers'])
    locs['witchs_hut'] = bool(item_dict['mushroom']) and \
                         (bool(item_dict['gloves']) or bool(item_dict['flippers']) or bool(item_dict['hammer']))
    locs['waterfall_fairy'] = bool(item_dict['flippers'])
    locs['king_zora'] = (bool(item_dict['gloves']) or bool(item_dict['flippers']) or bool(item_dict['hammer']))
    locs['zora_ledge'] = bool(item_dict['flippers']) and (bool(item_dict['gloves']) or bool(item_dict['hammer']))
    locs['old_man'] = bool(item_dict['lantern']) and (bool(item_dict['gloves']) or bool(item_dict['flute']))
    locs['spectacle_rock'] = bool(item_dict['mirror']) and dw_access['dm_west']
    locs['spectacle_cave'] = dw_access['dm_west']
    locs['ether_tablet'] = bool(item_dict['book']) and item_dict['sword'] >= 2 and dw_access['dm_west'] and \
                           (bool(item_dict['mirror']) or (bool(item_dict['hookshot']) and bool(item_dict['hammer'])))
    locs['paradox_cave'] = dw_access['dm_west'] and \
                           (bool(item_dict['hookshot']) or (bool(item_dict['mirror']) and bool(item_dict['hammer'])))
    locs['spiral_cave'] = locs['paradox_cave']
    locs['mimic_cave'] = dw_access['dm_east'] and item_dict['gloves'] >= 2 and bool(item_dict['hammer']) and \
                         bool(item_dict['somaria']) and bool(item_dict['fire_rod']) and \
                         medals['tr'] and bool(item_dict['moon_pearl'])
    locs['floating_island'] = dw_access['dm_east'] and bool(item_dict['gloves']) and bool(item_dict['mirror'])
    locs['bonk_rocks'] = bool(item_dict['boots'])
    locs['kings_tomb'] = bool(item_dict['boots']) and \
                         (item_dict['gloves'] >= 2 or (bool(item_dict['mirror']) and dw_access['north']))
    locs['graveyard_ledge'] = dw_access['north'] and bool(item_dict['mirror'])
    locs['sasha'] = bool(green_pendant)
    # sphere 0 items (no requirements)
    for location_name in LIGHT_WORLD_COORDS.keys():
        if location_name not in locs.keys():
            locs[location_name] = True
    return locs


def light_world_dungeon_availability(item_dict):
    locs = dict()
    dw_access = dark_world_areas(item_dict)
    locs['ep'] = True
    locs['ep_clear'] = (item_dict['bow'] == 1 or item_dict['bow'] == 3) and item_dict['lantern']
    locs['dp'] = bool(item_dict['book']) or (dw_access['mire'] and item_dict['mirror'])
    locs['dp_clear'] = locs['dp'] and bool(item_dict['gloves']) and (bool(item_dict['lantern']) or bool(item_dict['fire_rod']))
    locs['th'] = dw_access['dm_west'] and (bool(item_dict['mirror']) or (bool(item_dict['hookshot']) and bool(item_dict['hammer'])))
    locs['th_clear'] = locs['th'] and (bool(item_dict['lantern']) or bool(item_dict['fire_rod']))
    return locs


def compose_light_world_image(light_world_bg, item_dict, selected_location, checked_locations):
    working_image = pygame.Surface((light_world_bg.get_width(), light_world_bg.get_height()))
    working_image.blit(light_world_bg, (0, 0))
    # location drawing
    locations = light_world_availability(item_dict)
    for location_name, location_available in locations.iteritems():
        # draw border (selection indicator)
        border_color = BG_COLOR
        if location_name == selected_location:
            border_color = BORDER_SELECTED_COLOR
        border_size = LOCATION_SIZE + 2 * LOCATION_BORDER
        border_rect = pygame.Rect(0, 0, border_size, border_size)
        border_rect.center = LIGHT_WORLD_COORDS[location_name]
        pygame.draw.rect(working_image, border_color, border_rect)
        # draw inner rect (actual indicator)
        location_color = LOCATION_UNAVAILABLE_COLOR
        if location_name in checked_locations:
            location_color = LOCATION_CHECKED_COLOR
        elif locations[location_name]:
            location_color = LOCATION_AVAILABLE_COLOR
        location_rect = pygame.Rect(0, 0, LOCATION_SIZE, LOCATION_SIZE)
        location_rect.center = LIGHT_WORLD_COORDS[location_name]
        pygame.draw.rect(working_image, location_color, location_rect)
    # dungeon drawing
    dungeons = light_world_dungeon_availability(item_dict)
    for dungeon_name in ['ep', 'dp', 'th']:
        # border
        border_color = BG_COLOR
        if dungeon_name == selected_location:
            border_color = BORDER_SELECTED_COLOR
        border_size = DUNGEON_SIZE + 2 * DUNGEON_BORDER
        border_rect = pygame.Rect(0, 0, border_size, border_size)
        border_rect.center = LIGHT_WORLD_DUNGEON_COORDS[dungeon_name]
        pygame.draw.rect(working_image, border_color, border_rect)
        # outer large rect (dungeon accessible indicator)
        dungeon_color = LOCATION_UNAVAILABLE_COLOR
        if bool(item_dict[dungeon_name]):
            dungeon_color = LOCATION_CHECKED_COLOR
        elif dungeons[dungeon_name]:
            dungeon_color = LOCATION_AVAILABLE_COLOR
        dungeon_rect = pygame.Rect(0, 0, DUNGEON_SIZE, DUNGEON_SIZE)
        dungeon_rect.center = border_rect.center
        pygame.draw.rect(working_image, dungeon_color, dungeon_rect)
        # inner small rect (dungeon clearable indicator)
        clear_color = LOCATION_UNAVAILABLE_COLOR
        if item_dict['{}_chests'.format(dungeon_name)] == ITEM_MAX['{}_chests'.format(dungeon_name)]:
            clear_color = LOCATION_CHECKED_COLOR
        elif dungeons['{}_clear'.format(dungeon_name)]:
            clear_color = LOCATION_AVAILABLE_COLOR
        clear_rect = pygame.Rect(0, 0, DUNGEON_INNER_SIZE, DUNGEON_INNER_SIZE)
        clear_rect.center = border_rect.center
        pygame.draw.rect(working_image, clear_color, clear_rect)
    return working_image


def dark_world_availability(item_dict):
    _, _, red_crystals = pendants(item_dict)
    dw_access = dark_world_areas(item_dict)
    locs = dict()
    locs['chest_game'] = dw_access['north'] and bool(item_dict['moon_pearl'])
    locs['c_house'] = dw_access['north']
    locs['bomb_hut'] = dw_access['north'] and bool(item_dict['moon_pearl'])
    locs['peg_cave'] = dw_access['north'] and bool(item_dict['moon_pearl']) and \
                       item_dict['gloves'] >= 2 and bool(item_dict['hammer'])
    locs['dig_game'] = dw_access['south'] and bool(item_dict['moon_pearl'])
    locs['flute_kid'] = dw_access['south']
    locs['mire_shed'] = dw_access['mire']
    locs['hype_cave'] = dw_access['south'] and bool(item_dict['moon_pearl'])
    locs['pyramid'] = dw_access['east']
    locs['pyramid_fairy'] = dw_access['east'] and red_crystals >= 2
    locs['catfish'] = dw_access['east'] and bool(item_dict['gloves'])
    locs['bumper_cave'] = dw_access['north'] and bool(item_dict['cape'])
    locs['spike_cave'] = dw_access['dm_west'] and bool(item_dict['moon_pearl']) and \
                         bool(item_dict['hammer']) and (bool(item_dict['cape']) or bool(item_dict['byrna']))
    locs['hookshot_cave_bottom'] = dw_access['dm_west'] and bool(item_dict['moon_pearl']) and bool(item_dict['boots'])
    locs['hookshot_cave_full'] = locs['hookshot_cave_bottom'] and bool(item_dict['hookshot'])
    locs['super_bunny_cave'] = dw_access['east']
    return locs


def dark_world_dungeon_availability(item_dict):
    locs = dict()
    dw_access = dark_world_areas(item_dict)
    medals = dungeon_medallions(item_dict)
    locs['pd'] = dw_access['east']
    locs['pd_clear'] = locs['pd'] and bool(item_dict['hammer']) and \
                       (item_dict['bow'] == 1 or item_dict['bow'] == 3) and bool(item_dict['moon_pearl'])
    locs['sp'] = dw_access['south'] and bool(item_dict['mirror']) and bool(item_dict['flippers'])
    locs['sp_clear'] = locs['sp'] and bool(item_dict['hookshot']) and bool(item_dict['moon_pearl'])   # TODO -- check this (fire source needed?)
    locs['sw'] = dw_access['north']
    locs['sw_clear'] = locs['sw'] and bool(item_dict['fire_rod']) and bool(item_dict['moon_pearl'])
    locs['tt'] = dw_access['north'] and bool(item_dict['moon_pearl'])
    locs['tt_clear'] = locs['tt'] and bool(item_dict['hammer'])
    locs['ip'] = dw_access['ice'] and (bool(item_dict['bombos']) or bool(item_dict['fire_rod'])) and bool(item_dict['moon_pearl'])
    locs['ip_clear'] = locs['ip']   # TODO -- check this (anything actually required?)
    locs['mm'] = dw_access['mire'] and medals['mm'] and bool(item_dict['moon_pearl'])
    locs['mm_clear'] = locs['mm'] and bool(item_dict['somaria'])    # TODO -- anything else needed?
    locs['tr'] = dw_access['dm_east'] and item_dict['gloves'] >= 2 and bool(item_dict['hammer']) and \
                 bool(item_dict['somaria']) and medals['tr'] and bool(item_dict['moon_pearl'])
    locs['tr_clear'] = locs['tr'] and bool(item_dict['fire_rod']) and bool(item_dict['ice_rod'])
    return locs


def compose_dark_world_image(dark_world_bg, item_dict, selected_location, checked_locations):
    working_image = pygame.Surface((MAP_SIZE, MAP_SIZE))
    working_image.blit(dark_world_bg, (0, 0))
    locations = dark_world_availability(item_dict)
    for location_name, locations_available in locations.iteritems():
        # draw border/selection indicator
        border_color = BG_COLOR
        if location_name == selected_location:
            border_color = BORDER_SELECTED_COLOR
        border_size = LOCATION_SIZE + 2 * LOCATION_BORDER
        border_rect = pygame.Rect(0, 0, border_size, border_size)
        border_rect.center = DARK_WORLD_COORDS[location_name]
        pygame.draw.rect(working_image, border_color, border_rect)
        # draw inner rect (actual indicator)
        location_color = LOCATION_UNAVAILABLE_COLOR
        if location_name in checked_locations:
            location_color = LOCATION_CHECKED_COLOR
        elif locations[location_name]:
            location_color = LOCATION_AVAILABLE_COLOR
        location_rect = pygame.Rect(0, 0, LOCATION_SIZE, LOCATION_SIZE)
        location_rect.center = DARK_WORLD_COORDS[location_name]
        pygame.draw.rect(working_image, location_color, location_rect)
    # dungeon drawing
    dungeons = dark_world_dungeon_availability(item_dict)
    for dungeon_name in ['pd', 'sp', 'sw', 'tt', 'ip', 'mm', 'tr']:
        # border
        border_color = BG_COLOR
        if dungeon_name == selected_location:
            border_color = BORDER_SELECTED_COLOR
        border_size = DUNGEON_SIZE + 2 * DUNGEON_BORDER
        border_rect = pygame.Rect(0, 0, border_size, border_size)
        border_rect.center = DARK_WORLD_DUNGEON_COORDS[dungeon_name]
        pygame.draw.rect(working_image, border_color, border_rect)
        # outer large rect (dungeon accessible indicator)
        dungeon_color = LOCATION_UNAVAILABLE_COLOR
        if bool(item_dict[dungeon_name]):
            dungeon_color = LOCATION_CHECKED_COLOR
        elif dungeons[dungeon_name]:
            dungeon_color = LOCATION_AVAILABLE_COLOR
        dungeon_rect = pygame.Rect(0, 0, DUNGEON_SIZE, DUNGEON_SIZE)
        dungeon_rect.center = border_rect.center
        pygame.draw.rect(working_image, dungeon_color, dungeon_rect)
        # inner small rect (dungeon clearable indicator)
        clear_color = LOCATION_UNAVAILABLE_COLOR
        if item_dict['{}_chests'.format(dungeon_name)] == ITEM_MAX['{}_chests'.format(dungeon_name)]:
            clear_color = LOCATION_CHECKED_COLOR
        elif dungeons['{}_clear'.format(dungeon_name)]:
            clear_color = LOCATION_AVAILABLE_COLOR
        clear_rect = pygame.Rect(0, 0, DUNGEON_INNER_SIZE, DUNGEON_INNER_SIZE)
        clear_rect.center = border_rect.center
        pygame.draw.rect(working_image, clear_color, clear_rect)
    return working_image


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
