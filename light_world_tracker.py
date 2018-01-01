import pygame


MAP_SIZE = 276
LOCATION_SIZE = 10
BORDER_SIZE = 2
BORDER_COLOR = (0, 0, 0)
UNAVAILABLE_COLOR = (255, 0, 0)
AVAILABLE_COLOR = (0, 255, 0)
VISIBLE_COLOR = (255, 255, 0)
CHECKED_COLOR = (128, 128, 128)
LOCATION_COORDS = {'links_house': (152, 192), 'escape_front': (136, 121), 'escape_dark': (136, 106),
                   'escape_back': (136, 90), 'uncle_tunnel': (154, 123), 'lumberjack_cave': (85, 30),
                   'lost_woods_ledge': (52, 49), 'mushroom_spot': (36, 36), 'pedestal': (20, 20),
                   'kakariko_well': (14, 120), 'blinds_house': (38, 120), 'bottle_vendor': (31, 135),
                   'chicken_house':(32, 155), 'sick_kid': (52, 148), 'tavern': (52, 162), 'blacksmiths': (85, 148),
                   'magic_bat': (100, 156), 'library': (54, 184), 'hedge_race': (22, 180), 'grove_dig': (85, 180),
                   'grove_ledge': (69, 207), 'desert_ledge': (10, 236), 'checkerboard_cave': (55, 218),
                   'aginahs_cave': (68, 234), 'bombos_tablet': (65, 255), 'purple_chest': (99, 242), 'dam': (130, 258),
                   'mini_moldorm_cave': (178, 250), 'ice_rod_cave': (247, 209), 'hylia_island': (194, 228),
                   'hobo': (193, 196), 'witchs_hut': (215, 95), 'waterfall_fairy': (238, 60), 'king_zora': (261, 45),
                   'zora_ledge': (257, 58), 'old_man': (112, 60), 'spectacle_rock': (138, 33),
                   'spectacle_cave': (126, 44), 'ether_tablet': (126, 20), 'paradox_cave': (220, 66),
                   'spiral_cave': (202, 36), 'mimic_cave': (214, 52), 'floating_island': (210, 10),
                   'bonk_rocks': (105, 85), 'sanctuary': (120, 87), 'kings_tomb': (162, 93),
                   'graveyard_ledge': (150, 85), 'sashas_hut': (214, 116), 'sasha': (214, 130)}
LOCATION_AMOUNTS = {'uncle_tunnel': 2}


def dark_world_access(item_dict):
    dw_points = dict()
    dw_points['castle'] = bool(item_dict['aga'])
    dw_points['lost_woods'] = item_dict['gloves'] >= 2 or (bool(item_dict['hammer']) and bool(item_dict['gloves']))
    dw_points['east'] = bool(item_dict['gloves']) and bool(item_dict['hammer'])
    dw_points['swamp'] = dw_points['east']
    dw_points['lake'] = bool(item_dict['flippers']) and item_dict['gloves'] >= 2
    dw_points['desert'] = bool(item_dict['flute']) and item_dict['gloves'] >= 2
    dw_points['dm_west'] = bool(item_dict['flute']) or (bool(item_dict['gloves']) and bool(item_dict['lantern']))
    dw_points['dm_east'] = dw_points['dm_west'] and item_dict['gloves'] >= 2 and (bool(item_dict['hookshot']) \
                            or (bool(item_dict['mirror']) and bool(item_dict['hammer'])))
    dw_points['t_rock'] = dw_points['dm_west'] and bool(item_dict['hammer']) and item_dict['gloves'] >= 2 \
                            and (bool(item_dict['hookshot']) or (bool(item_dict['mirror']) and bool(item_dict['hammer'])))
    return dw_points


def location_availability(item_dict):
    dw_spots = dark_world_access(item_dict)
    lw_locs = dict()
    lw_locs['links_house'] = True
    lw_locs['escape_front'] = True
    lw_locs['escape_dark'] = bool(item_dict['lantern'])
    lw_locs['escape_back'] = bool(item_dict['lantern']) or bool(item_dict['gloves'])
    lw_locs['uncle_tunnel'] = True
    lw_locs['lumberjack_cave'] = bool(item_dict['aga']) and bool(item_dict['boots'])
    lw_locs['lost_woods_ledge'] = True
    lw_locs['mushroom_spot'] = True
    lw_locs['pedestal'] = bool(item_dict['green_pendant']) and item_dict['other_pendants'] >= 2
    lw_locs['kakariko_well'] = True
    lw_locs['blinds_house'] = True
    lw_locs['bottle_vendor'] = True
    lw_locs['chicken_house'] = True
    lw_locs['sick_kid'] = bool(item_dict['bottles'])
    lw_locs['tavern'] = True
    lw_locs['blacksmiths'] = item_dict['gloves'] >= 2
    lw_locs['magic_bat'] = bool(item_dict['powder'])
    lw_locs['library'] = bool(item_dict['boots'])
    lw_locs['hedge_race'] = True
    lw_locs['grove_dig'] = bool(item_dict['shovel'])
    lw_locs['grove_ledge'] = bool(item_dict['mirror']) and \
        (dw_spots['lost_woods'] or dw_spots['swamp'] or (dw_spots['castle'] and (item_dict['hammer'] or item_dict['hookshot'])))
    lw_locs['desert_ledge'] = bool(item_dict['book']) or (dw_spots['desert'] and bool(item_dict['mirror']))
    lw_locs['checkerboard_cave'] = lw_locs['desert_ledge'] and bool(item_dict['mirror'])
    lw_locs['aginahs_cave'] = True
    lw_locs['bombos_tablet'] = bool(item_dict['mirror']) and item_dict['sword'] >= 2 and \
        (dw_spots['lost_woods'] or dw_spots['swamp'] or (dw_spots['castle'] and (item_dict['hammer'] or item_dict['hookshot'])))
    lw_locs['purple_chest'] = item_dict['gloves'] >= 2
    lw_locs['dam'] = True
    lw_locs['mini_moldorm_cave'] = True
    lw_locs['ice_rod_cave'] = True
    lw_locs['hylia_island'] = bool(item_dict['flippers']) and bool(item_dict['mirror']) and \
        (dw_spots['lost_woods'] or dw_spots['swamp'] or (dw_spots['castle'] and (item_dict['hammer'] or item_dict['hookshot'])))
    lw_locs['hobo'] = bool(item_dict['flippers'])
    lw_locs['witchs_hut'] = bool(item_dict['mushroom'])
    lw_locs['waterfall_fairy'] = bool(item_dict['flippers']) and bool(item_dict['gloves'])
    lw_locs['king_zora'] = bool(item_dict['gloves'])
    lw_locs['zora_ledge'] = bool(item_dict['flippers']) and bool(item_dict['gloves'])
    lw_locs['old_man'] = bool(item_dict['lantern']) and (bool(item_dict['gloves']) or bool(item_dict['flute']))
    lw_locs['spectacle_rock'] = dw_spots['dm_west']
    lw_locs['spectacle_cave'] = dw_spots['dm_west']
    lw_locs['ether_tablet'] = bool(item_dict['book']) and item_dict['sword'] >= 2 and dw_spots['dm_west'] and \
                              (bool(item_dict['mirror']) or (bool(item_dict['hookshot']) and bool(item_dict['hammer'])))
    lw_locs['paradox_cave'] = dw_spots['dm_west'] and \
                              ((bool(item_dict['hookshot']) or (bool(item_dict['mirror'])) and bool(item_dict['hammer'])))
    lw_locs['spiral_cave'] = lw_locs['paradox_cave']
    lw_locs['mimic_cave'] = dw_spots['t_rock'] and bool(item_dict['tr_medallion']) \
                            and bool(item_dict['cane_somaria']) and bool(item_dict['mirror'])
    lw_locs['floating_island'] = bool(item_dict['mirror']) # ...and... TODO
    lw_locs['bonk_rocks'] = bool(item_dict['boots'])
    lw_locs['sanctuary'] = True
    lw_locs['kings_tomb'] = bool(item_dict['boots']) and (item_dict['gloves'] >= 2 or (bool(item_dict['mirror']) and \
                                            (dw_spots['lost_woods'] or (dw_spots['castle'] and \
                                            (bool(item_dict['hookshot']) or bool(item_dict['hammer']))) or dw_spots['swamp'])))
    lw_locs['graveyard_ledge'] = bool(item_dict['mirror']) and \
                                            (dw_spots['lost_woods'] or (dw_spots['castle'] and \
                                            (bool(item_dict['hookshot']) or bool(item_dict['hookshot']))) or dw_spots['swamp'])
    lw_locs['sashas_hut'] = True
    lw_locs['sasha'] = bool(item_dict['green_pendant'])
    return lw_locs


def compose_light_world_image(bg_image, item_dict, checked_locations_list):
    working_image = pygame.Surface((MAP_SIZE, MAP_SIZE))
    working_image.blit(bg_image, (0, 0))
    location_dict = location_availability(item_dict)
    visible_items = ['lumberjack_cave', 'library', 'desert_ledge']
    if item_dict['book']:
        visible_items.append('pedestal')
    if item_dict['flippers']:
        visible_items.append('hylia_island')
    for location_name, available in location_dict.iteritems():
        outer_size = LOCATION_SIZE + 2 * BORDER_SIZE
        outer_rect = pygame.Rect(LOCATION_COORDS[location_name], (outer_size, outer_size))
        pygame.draw.rect(working_image, BORDER_COLOR, outer_rect)
        location_color = CHECKED_COLOR
        if location_name not in checked_locations_list:
            if available:
                location_color = AVAILABLE_COLOR
            else:
                if location_name in visible_items:
                    location_color = VISIBLE_COLOR
                else:
                    location_color = UNAVAILABLE_COLOR
        inner_coords = (LOCATION_COORDS[location_name][0] + BORDER_SIZE, LOCATION_COORDS[location_name][1] + BORDER_SIZE)
        inner_rect = pygame.Rect(inner_coords, (LOCATION_SIZE, LOCATION_SIZE))
        pygame.draw.rect(working_image, location_color, inner_rect)
    return working_image
