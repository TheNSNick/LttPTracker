import pygame
import os


TILE_SIZE = 32
BOTTOM_HEIGHT = 52
BG_COLOR = (0, 0, 0)
ALPHA_COLOR = (255, 0, 255)
MASKING_ALPHA = 128
GFX_DIR = 'gfx'
ITEM_COORDS = {
    (0, 0): 'mail', (1, 0): 'sword', (2, 0): 'bow', (3, 0): 'boomerang', (4, 0): 'hookshot', (5, 0): 'mushroom', (6, 0): 'powder',
    (0, 1): 'shield', (1, 1): 'moon_pearl', (2, 1): 'fire_rod', (3, 1): 'ice_rod', (4, 1): 'bombos', (5, 1): 'ether', (6, 1): 'quake',
    (0, 2): 'armos', (1, 2): 'ep', (2, 2): 'lantern', (3, 2): 'hammer', (4, 2): 'shovel', (5, 2): 'net', (6, 2): 'book',
    (0, 3): 'lanmola', (1, 3): 'dp', (2, 3): 'bottles', (3, 3): 'somaria', (4, 3): 'byrna', (5, 3): 'cape', (6, 3): 'mirror',
    (0, 4): 'moldorm', (1, 4): 'th', (2, 4): 'boots', (3, 4): 'gloves', (4, 4): 'flippers', (5, 4): 'flute', (6, 4): 'aga',
    (0, 5): 'helmasaur', (1, 5): 'arrghus', (2, 5): 'mothula', (3, 5): 'blind', (4, 5): 'kholdstare', (5, 5): 'vitreous', (6, 5): 'trinexx',
    (0, 6): 'pd', (1, 6): 'sp', (2, 6): 'sw', (3, 6): 'tt', (4, 6): 'ip', (5, 6): 'mm', (6, 6): 'tr',
    (0, 7): 'ep_tracker', (1, 7): 'dp_tracker', (2, 7): 'th_tracker', (3, 7): 'pd_tracker', (4, 7): 'sp_tracker',
    (5, 7): 'sw_tracker', (6, 7): 'tt_tracker', (7, 7): 'ip_tracker', (8, 7): 'mm_tracker', (9, 7): 'tr_tracker'}
ITEM_MAX = {'mail': 2, 'sword': 4, 'shield': 3, 'bow': 3, 'boomerang': 3,
            'mushroom': 2, 'powder': 2, 'shovel': 2, 'bottles': 4, 'gloves': 2,
            'ep': 3, 'dp': 2, 'th': 2, 'pd': 5, 'sp': 6, 'sw': 2, 'tt': 4, 'ip': 3, 'mm': 2, 'tr': 5,
            'ep_tracker': 4, 'dp_tracker': 4, 'th_tracker': 4, 'pd_tracker': 4, 'sp_tracker': 4,
            'sw_tracker': 4, 'tt_tracker': 4, 'ip_tracker': 4, 'mm_tracker': 4, 'tr_tracker': 4,
            'other_pendants': 2, 'blue_crystals': 5, 'red_crystals': 2}
ITEM_UNMASK = {'mail': 0, 'aga': 0, 'ep': 0, 'dp': 0, 'th': 0, 'pd': 0,
               'sp': 0, 'sw': 0, 'tt': 0, 'ip': 0, 'mm': 0, 'tr': 0}
ITEM_UPGRADE = {'mail': 1, 'sword': 1, 'shield': 2, 'bow': 2, 'boomerang': 2, 'shovel': 2,
                'mushroom': 2, 'powder': 2, 'bottles': 1, 'gloves': 2, 'aga': 1}
DUNGEON_ITEMS_AMOUNT = {'ep': 3, 'dp': 2, 'th': 2, 'pd': 5, 'sp': 6, 'sw': 2, 'tt': 4, 'ip': 3, 'mm': 2, 'tr': 5}
TRACKER_ITEM_NAMES = {1: 'green_pendant', 2: 'other_pendants', 3: 'blue_crystals', 4: 'red_crystals'}
BOSS_TO_TRACKER = {'armos': 'ep_tracker', 'lanmola': 'dp_tracker', 'moldorm': 'th_tracker', 'helmasaur': 'pd_tracker',
                   'arrghus': 'sp_tracker', 'mothula': 'sw_tracker', 'blind': 'tt_tracker', 'kholdstare': 'ip_tracker',
                   'vitreous': 'mm_tracker', 'trinexx': 'tr_tracker'}


def new_item_dict():
    items = dict()
    for _, item_name in ITEM_COORDS.iteritems():
        items[item_name] = 0
    extras = ['green_pendant', 'other_pendants', 'blue_crystals', 'red_crystals', 'mm_medallion', 'tr_medallion']
    for extra in extras:    # read all about it!
        items[extra] = 0
    return items


def compose_item_image(bg_image, tracker_image_dict, item_dict):
    # base image
    working_image = pygame.Surface((7 * TILE_SIZE, 7 * TILE_SIZE + BOTTOM_HEIGHT))
    working_image.blit(bg_image, (0, 0))
    # masking and upgrading
    masking_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    masking_image.fill(BG_COLOR)
    masking_image.set_alpha(MASKING_ALPHA)
    blanking_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    blanking_image.fill(BG_COLOR)
    mask_aga = True
    if item_dict['aga'] or item_dict['sword'] >= 2 or (item_dict['sword'] >= 1 and bool(item_dict['cape'])):
        mask_aga = False
    for x in range(7):
        for y in range(7):
            item_name = ITEM_COORDS[(x, y)]
            draw_coords = (x * TILE_SIZE, y * TILE_SIZE)
            if item_dict[item_name] < ITEM_UNMASK.get(item_name, 1) or (item_name == 'aga' and mask_aga):
                working_image.blit(masking_image, draw_coords)
            if item_name in ITEM_UPGRADE.keys() and item_dict[item_name] >= ITEM_UPGRADE[item_name]:
                working_image.blit(blanking_image, draw_coords)
                upgrade_image_file = os.path.join(GFX_DIR, '{}_{}.png'.format(item_name, item_dict[item_name]))
                upgrade_image = pygame.image.load(upgrade_image_file).convert()
                upgrade_image.set_colorkey(ALPHA_COLOR)
                working_image.blit(upgrade_image, draw_coords)
            if item_name in DUNGEON_ITEMS_AMOUNT.keys() and item_dict[item_name] > 0:
                chest_image_file = os.path.join(GFX_DIR, 'chest_{}_{}.png'.format(DUNGEON_ITEMS_AMOUNT[item_name], item_dict[item_name]))
                chest_image = pygame.image.load(chest_image_file).convert()
                chest_image.set_colorkey(ALPHA_COLOR)
                working_image.blit(chest_image, draw_coords)
    tracker_image_names = {1: 'green_pendant', 2: 'other_pendant', 3: 'blue_crystal', 4: 'red_crystal'}
    for x in range(10):
        tracker_name = ITEM_COORDS[(x, 7)]
        if item_dict[tracker_name]:
            tracker_image = tracker_image_dict[TRACKER_ITEM_NAMES[item_dict[tracker_name]]]
            tracker_rect = tracker_image.get_rect()
            tracker_rect.midleft = x * tracker_image.get_width(), 7 * TILE_SIZE + BOTTOM_HEIGHT / 2
            tracker_rect.left += max((x - 7) * 2, 0)
            working_image.blit(tracker_image, tracker_rect)
    return working_image


def decrement_item(item_dict, item_name):
    item_dict[item_name] -= 1
    if item_name in BOSS_TO_TRACKER.keys() and item_dict[BOSS_TO_TRACKER[item_name]]:
        decrement_item(item_dict, TRACKER_ITEM_NAMES[item_dict[BOSS_TO_TRACKER[item_name]]])
    if item_dict[item_name] < 0:
        item_dict[item_name] = ITEM_MAX.get(item_name, 1)


def increment_item(item_dict, item_name):
    item_dict[item_name] += 1
    if item_name in BOSS_TO_TRACKER.keys() and item_dict[BOSS_TO_TRACKER[item_name]]:
        increment_item(item_dict, TRACKER_ITEM_NAMES[item_dict[BOSS_TO_TRACKER[item_name]]])
    if item_dict[item_name] > ITEM_MAX.get(item_name, 1):
        item_dict[item_name] = 0
