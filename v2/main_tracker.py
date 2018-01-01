import pygame
import sys
import os


TILE_SIZE = 32
SCREEN_WIDTH = 7 * TILE_SIZE
SCREEN_HEIGHT = 7 * TILE_SIZE
COLORS = {'BG': (0, 0, 0), 'ALPHA': (255, 0, 255)}
MASKING_ALPHA = 128
FPS = 30
ITEM_BG_IMAGE_PATH = os.path.join('gfx', 'item_bg.png')
ITEM_IMAGE_COORDS = (0, 0)
ITEM_COORDS = {
    (0, 0): 'mail', (1, 0): 'sword', (2, 0): 'bow', (3, 0): 'boomerang', (4, 0): 'hookshot', (5, 0): 'mushroom',
    (6, 0): 'powder',
    (0, 1): 'shield', (1, 1): 'moon_pearl', (2, 1): 'fire_rod', (3, 1): 'ice_rod', (4, 1): 'bombos',
    (5, 1): 'ether', (6, 1): 'quake',
    (2, 2): 'lantern', (3, 2): 'hammer', (4, 2): 'shovel', (5, 2): 'net', (6, 2): 'book',
    (2, 3): 'bottles', (3, 3): 'somaria', (4, 3): 'byrna', (5, 3): 'cape', (6, 3): 'mirror',
    (2, 4): 'boots', (3, 4): 'gloves', (4, 4): 'flippers', (5, 4): 'flute', (6, 4): 'aga'}
ITEM_MAX = {'mail': 2, 'sword': 4, 'shield': 3, 'bow': 3, 'boomerang': 3, 'bottles': 4, 'gloves': 2}
ITEM_UPGRADE = {'mail': 1, 'sword': 1, 'shield': 2, 'bow': 2, 'boomerang': 2, 'bottles': 1, 'gloves': 2, 'aga': 1}
DUNGEON_COORDS = {(0, 2): 'ep', (1, 2): 'ep_chests', (0, 3): 'dp', (1, 3): 'dp_chests',
                  (0, 4): 'th', (1, 4): 'th_chests', (0, 5): 'pd', (0, 6): 'pd_chests',
                  (1, 5): 'sp', (1, 6): 'sp_chests', (2, 5): 'sw', (2, 6): 'sw_chests',
                  (3, 5): 'tt', (3, 6): 'tt_chests', (4, 5): 'ip', (4, 6): 'ip_chests',
                  (5, 5): 'mm', (5, 6): 'mm_chests', (6, 5): 'tr', (6, 6): 'tr_chests'}
DUNGEON_ITEM_AMOUNTS = {'ep': 3, 'dp': 2, 'th': 2, 'pd': 5, 'sp': 6, 'sw': 2, 'tt': 4, 'ip': 3, 'mm': 2, 'tr': 5}


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    item_bg_image = pygame.image.load(ITEM_BG_IMAGE_PATH).convert()
    item_bg_image.set_colorkey(COLORS['ALPHA'])
    items = load_items()
    dungeon_items = load_dungeon_items()
    checked_locations = list()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos, event.button, items, dungeon_items)
        screen.fill(COLORS['BG'])
        item_pane = item_image(item_bg_image, items)
        final_pane = apply_dungeon_masking(item_pane, dungeon_items)
        screen.blit(final_pane, ITEM_IMAGE_COORDS)
        pygame.display.update()
        clock.tick(FPS)


def handle_click(click_coords, click_button, item_dict, dungeon_dict):
    # item clicks
    item_rect_1 = pygame.Rect(ITEM_IMAGE_COORDS, (2 * TILE_SIZE, 2 * TILE_SIZE))
    item_rect_2 = pygame.Rect(ITEM_IMAGE_COORDS[0] + 2 * TILE_SIZE, ITEM_IMAGE_COORDS[1], 5 * TILE_SIZE, 5 * TILE_SIZE)
    if item_rect_1.collidepoint(click_coords) or item_rect_2.collidepoint(click_coords):
        item_coords = click_coords[0] / TILE_SIZE, click_coords[1] / TILE_SIZE
        item_name = ITEM_COORDS[item_coords]
        if click_button == 1:
            item_dict[item_name] += 1
            if item_dict[item_name] > ITEM_MAX.get(item_name, 1):
                item_dict[item_name] = 0
        elif click_button == 3:
            item_dict[item_name] -= 1
            if item_dict[item_name] < 0:
                item_dict[item_name] = ITEM_MAX.get(item_name, 1)
    dungeon_rect_1 = pygame.Rect(ITEM_IMAGE_COORDS[0], ITEM_IMAGE_COORDS[1] + 2 * TILE_SIZE, 2 * TILE_SIZE, 3 * TILE_SIZE)
    dungeon_rect_2 = pygame.Rect(ITEM_IMAGE_COORDS[0], ITEM_IMAGE_COORDS[1] + 5 * TILE_SIZE, 7 * TILE_SIZE, 2 * TILE_SIZE)
    if dungeon_rect_1.collidepoint(click_coords) or dungeon_rect_2.collidepoint(click_coords):
        dungeon_coords = click_coords[0] / TILE_SIZE, click_coords[1] / TILE_SIZE
        dungeon_name = DUNGEON_COORDS[dungeon_coords]
        if click_button == 1:
            dungeon_dict[dungeon_name] += 1
            if dungeon_dict[dungeon_name] > DUNGEON_ITEM_AMOUNTS.get(dungeon_name[:2], 1):
                dungeon_dict[dungeon_name] = 0
        elif click_button == 3:
            dungeon_dict[dungeon_name] -= 1
            if dungeon_dict[dungeon_name] < 0:
                dungeon_dict[dungeon_name] = DUNGEON_ITEM_AMOUNTS.get(dungeon_name[:2], 1)


def load_items():
    items = dict()
    for _, item_name in ITEM_COORDS.iteritems():
        items[item_name] = 0
    return items


def item_image(bg_image, item_dict):
    working_image = pygame.Surface((7 * TILE_SIZE, 7 * TILE_SIZE))
    working_image.blit(bg_image, (0, 0))
    masking_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    masking_image.fill(COLORS['BG'])
    for coords, item_name in ITEM_COORDS.iteritems():
        draw_coords = coords[0] * TILE_SIZE, coords[1] * TILE_SIZE
        # masking
        if item_dict[item_name] == 0 and item_name not in ['mail', 'aga']:
            masking_image.set_alpha(MASKING_ALPHA)
            working_image.blit(masking_image, draw_coords)
        # upgrades
        elif item_name in ITEM_UPGRADE.keys() and item_dict[item_name] >= ITEM_UPGRADE[item_name]:
            masking_image.set_alpha(255)
            working_image.blit(masking_image, draw_coords)
            upgrade_image_path = os.path.join('gfx', '{}_{}.png'.format(item_name, item_dict[item_name]))
            upgrade_image = pygame.image.load(upgrade_image_path).convert()
            upgrade_image.set_colorkey(COLORS['ALPHA'])
            working_image.blit(upgrade_image, draw_coords)
    return working_image


def load_dungeon_items():
    dungeon_items = dict()
    for _, item_name in DUNGEON_COORDS.iteritems():
        dungeon_items[item_name] = 0
    dungeon_items['mm_medallion'] = None
    dungeon_items['tr_medallion'] = None
    return dungeon_items


def apply_dungeon_masking(bg_image, dungeon_item_dict):
    working_image = pygame.Surface((7 * TILE_SIZE, 7 * TILE_SIZE))
    working_image.blit(bg_image, (0, 0))
    working_image.set_colorkey(COLORS['ALPHA'])
    masking_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    masking_image.fill(COLORS['BG'])
    masking_image.set_alpha(128)
    for coords, item_name in DUNGEON_COORDS.iteritems():
        draw_coords = coords[0] * TILE_SIZE, coords[1] * TILE_SIZE
        if 'chests' in item_name:
            if dungeon_item_dict[item_name] > 0:
                chest_image_path = os.path.join('gfx', 'chest_{}_{}.png'.format(DUNGEON_ITEM_AMOUNTS[item_name[:2]], dungeon_item_dict[item_name]))
                chest_image = pygame.image.load(chest_image_path).convert()
                chest_image.set_colorkey(COLORS['ALPHA'])
                working_image.blit(chest_image, draw_coords)
        elif dungeon_item_dict[item_name] == 0:
            working_image.blit(masking_image, draw_coords)
    return working_image


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()