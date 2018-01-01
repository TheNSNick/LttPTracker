import pygame
import sys
import os
import item_tracker
import light_world_tracker


TILE_SIZE = 32
MAP_SIZE = 276
BG_COLOR = (0, 0, 0)
ALPHA_COLOR = (255, 0, 255)
FPS = 30
GFX_DIR = 'gfx'
ITEM_BG_FILE = os.path.join(GFX_DIR, 'item_bg.png')
LW_BG_FILE = os.path.join(GFX_DIR, 'light_world.png')
GREEN_MEDALLION_FILE = os.path.join(GFX_DIR, 'green_pendant.png')
OTHER_MEDALLION_FILE = os.path.join(GFX_DIR, 'other_pendant.png')
BLUE_CRYSTAL_FILE = os.path.join(GFX_DIR, 'blue_crystal.png')
RED_CRYSTAL_FILE = os.path.join(GFX_DIR, 'red_crystal.png')


def main():
    pygame.init()
    screen = pygame.display.set_mode((7 * TILE_SIZE + MAP_SIZE, max(7 * TILE_SIZE, MAP_SIZE)))
    clock = pygame.time.Clock()
    item_bg = pygame.image.load(ITEM_BG_FILE).convert()
    item_bg.set_colorkey(ALPHA_COLOR)
    light_world_bg = pygame.image.load(LW_BG_FILE)
    items = item_tracker.new_item_dict()
    checked_locations = list()
    # TODO -- USE BELOW IMAGES TO SET/DRAW DUNGEON CRYSTAL/PENDANTS/MEDALLIONS ( IN ITEMTRACKER )
    dungeon_image_dict = load_dungeon_indicator_images()
    # TODO -- USE ABOVE IMAGES TO SET/DRAW DUNGEON CRYSTAL/PENDANTS/MEDALLIONS ( IN ITEMTRACKER )
    item_image = item_tracker.compose_item_image(item_bg, dungeon_image_dict, items)
    light_world_image = light_world_tracker.compose_light_world_image(light_world_bg, items, checked_locations)
    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                change = False
                if event.pos[0] <= 7 * TILE_SIZE:
                    if event.pos[1] <= 7 * TILE_SIZE:
                        click_coords = event.pos[0] / TILE_SIZE, event.pos[1] / TILE_SIZE
                    else:
                        click_coords = event.pos[0] / (7 * TILE_SIZE / 10), 7
                    item_name = item_tracker.ITEM_COORDS[click_coords]
                    if event.button == 1:
                        item_tracker.increment_item(items, item_name)
                        change = True
                    elif event.button == 3:
                        item_tracker.decrement_item(items, item_name)
                        change = True
                elif 7 * TILE_SIZE < event.pos[0] <= 7 * TILE_SIZE + MAP_SIZE:
                    click_x = event.pos[0] - 7 * TILE_SIZE
                    for location_name, location_coords in light_world_tracker.LOCATION_COORDS.iteritems():
                        if max(click_x - location_coords[0], event.pos[1] - location_coords[1]) <= light_world_tracker.LOCATION_SIZE + 2 * light_world_tracker.BORDER_SIZE and min(click_x - location_coords[0], event.pos[1] - location_coords[1]) > 0:
                            if location_name in checked_locations:
                                checked_locations.remove(location_name)
                            else:
                                checked_locations.append(location_name)
                            change = True
                if change:
                    item_image = item_tracker.compose_item_image(item_bg, dungeon_image_dict, items)
                    light_world_image = light_world_tracker.compose_light_world_image(light_world_image, items, checked_locations)

        screen.fill(BG_COLOR)
        screen.blit(item_image, (0, 0))
        screen.blit(light_world_image, (7 * TILE_SIZE, 0))
        pygame.display.update()
        clock.tick()


def load_dungeon_indicator_images():
    images = dict()
    indicators = {'green_pendant': GREEN_MEDALLION_FILE, 'other_pendants': OTHER_MEDALLION_FILE,
                  'blue_crystals': BLUE_CRYSTAL_FILE, 'red_crystals': RED_CRYSTAL_FILE}
    for image_name, image_file in indicators.iteritems():
        indicator_image = pygame.image.load(image_file).convert()
        indicator_image.set_colorkey(ALPHA_COLOR)
        images[image_name] = indicator_image
    return images


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
