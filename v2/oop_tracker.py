import os
import sys
import copy
import pygame

# CONSTANTS
TILE_SIZE = 32
MAP_SIZE = 276
LOCATION_SIZE = 9
LOCATION_BORDER = 2
DUNGEON_SIZE = 24
DUNGEON_INNER_SIZE = 18
DUNGEON_BORDER = 3
SCREEN_WIDTH = max(10 * TILE_SIZE, MAP_SIZE)
SCREEN_HEIGHT = 5 * TILE_SIZE + 2 * MAP_SIZE
FPS = 5
SHADE_AMOUNT = 128
BG_COLOR = (0, 0, 0)
ALPHA_COLOR = (255, 0, 255)
CHECKED_COLOR = (128, 128, 128)
AVAILABLE_COLOR = (0, 222, 0)
UNAVAILABLE_COLOR = (222, 0, 0)
VISIBLE_COLOR = (222, 222, 0)
DRAW_COORDS = {
    'item_bg': (0, 0),
    'dungeons': (0, 3 * TILE_SIZE),
    'chests': (0, 4 * TILE_SIZE),
    'light_map': ((SCREEN_WIDTH - MAP_SIZE) / 2, 5 * TILE_SIZE),
    'dark_map': ((SCREEN_WIDTH - MAP_SIZE) / 2, 5 * TILE_SIZE + MAP_SIZE)
}
ITEM_PLACEMENT = {
    'bow': (0, 0),
    'silvers': (1, 0),
    'boomerang': (2, 0),
    'hookshot': (3, 0),
    'mushroom': (4, 0),
    'powder': (5, 0),
    'boots': (6, 0),
    'gloves': (7, 0),
    'flippers': (8, 0),
    'moon_pearl': (9, 0),
    'fire_rod': (0, 1),
    'ice_rod': (1, 1),
    'bombos': (2, 1),
    'ether': (3, 1),
    'quake': (4, 1),
    'lantern': (5, 1),
    'hammer': (6, 1),
    'shovel': (7, 1),
    'flute': (8, 1),
    'mail': (9, 1),
    'bottles': (0, 2),
    'somaria': (1, 2),
    'byrna': (2, 2),
    'cape': (3, 2),
    'mirror': (4, 2),
    'book': (5, 2),
    'sword': (6, 2),
    'shield': (7, 2),
    'half_magic': (8, 2),
    'aga': (9, 2)
}
DUNGEON_ORDER = ['ep', 'dp', 'th', 'pd', 'sp', 'sw', 'tt', 'ip', 'mm', 'tr']
LIGHT_LOCATION_COORDS = {
    'links_house': (155, 195),
    'escape_front': (143, 126),
    'escape_dark': (143, 112),
    'escape_back': (143, 99),
    'uncle_tunnel': (156, 125),
    'lumberjack_cave': (91, 36),
    'stump_ledge': (55, 50),
    'mushroom_spot': (37, 43),
    'pedestal': (24, 26),
    'kakariko_well': (23, 127),
    'blinds_house': (43, 124),
    'bottle_vendor': (35, 139),
    'chicken_house':(39, 155),
    'sick_kid': (55, 151),
    'tavern': (55, 164),
    'blacksmiths': (95, 155),
    'magic_bat': (100, 165),
    'library': (59, 188),
    'hedge_race': (27, 188),
    'forest_grove': (89, 185),
    'south_of_grove_cave': (71, 212),
    'desert_ledge': (14, 245),
    'checkerboard_cave': (57, 225),
    'aginahs_cave': (72, 236),
    'bombos_tablet': (79, 255),
    'desert_thief': (103, 249),
    'dam': (133, 259),
    'mini_moldorm_cave': (183, 253),
    'ice_rod_cave': (252, 211),
    'lake_hylia_island': (199, 230),
    'hobo': (195, 197),
    'witchs_hut': (219, 99),
    'waterfall_fairy': (248, 67),
    'king_zora': (261, 51),
    'zora_ledge': (262, 63),
    'old_man': (115, 62),
    'spectacle_rock': (144, 37),
    'spectacle_rock_cave': (139, 50),
    'ether_tablet': (130, 25),
    'paradox_cave': (224, 70),
    'spiral_cave': (206, 40),
    'mimic_cave': (218, 56),
    'floating_island': (214, 14),
    'bonk_rocks': (109, 89),
    'kings_tomb': (166, 97),
    'graveyard_ledge': (154, 89),
    'sahasrahlas_hut': (218, 120),
    'sahasrahla': (218, 134),
    'sanctuary': (131, 88)
}
LIGHT_DUNGEON_COORDS = {
    'ep': (248, 124),
    'dp': (32, 220),
    'th': (164, 16)
}
DARK_LOCATION_COORDS = {
    'chest_game': (25, 137),
    'c_house': (65, 137),
    'doorless_hut': (41, 168),
    'peg_cave': (94, 165),
    'digging_game': (27, 188),
    'haunted_grove': (94, 190),
    'mire_shed': (21, 218),
    'swamp_cave': (166, 219),
    'pyramid_ledge': (165, 120),
    'pyramid_fairy': (134, 138),
    'catfish': (250, 60),
    'bumper_cave': (98, 52),
    'spike_cave': (147, 45),
    'hookshot_cave_front': (213, 41),
    'hookshot_cave_back': (211, 30),
    'super_bunny_cave': (226, 61)
}
DARK_DUNGEON_COORDS = {
    'pd': (230, 144),
    'sp': (132, 256),
    'sw': (33, 33),
    'tt': (45, 142),
    'ip': (216, 238),
    'mm': (40, 242),
    'tr': (258, 28)
}


class Inventory:

    @staticmethod
    def generate_new_item_dict():
        items = dict()
        items['bow'] = {'value': 0, 'max': 1}
        items['silvers'] = {'value': 0, 'max': 1}
        items['boomerang'] = {'value': 0, 'max': 3}
        items['hookshot'] = {'value': 0, 'max': 1}
        items['mushroom'] = {'value': 0, 'max': 1}
        items['powder'] = {'value': 0, 'max': 1}
        items['boots'] = {'value': 0, 'max': 1}
        items['gloves'] = {'value': 0, 'max': 2}
        items['flippers'] = {'value': 0, 'max': 1}
        items['moon_pearl'] = {'value': 0, 'max': 1}
        items['fire_rod'] = {'value': 0, 'max': 1}
        items['ice_rod'] = {'value': 0, 'max': 1}
        items['bombos'] = {'value': 0, 'max': 1}
        items['ether'] = {'value': 0, 'max': 1}
        items['quake'] = {'value': 0, 'max': 1}
        items['lantern'] = {'value': 0, 'max': 1}
        items['hammer'] = {'value': 0, 'max': 1}
        items['shovel'] = {'value': 0, 'max': 1}
        items['flute'] = {'value': 0, 'max': 1}
        items['mail'] = {'value': 0, 'max': 2}
        items['bottles'] = {'value': 0, 'max': 4}
        items['somaria'] = {'value': 0, 'max': 1}
        items['byrna'] = {'value': 0, 'max': 1}
        items['cape'] = {'value': 0, 'max': 1}
        items['mirror'] = {'value': 0, 'max': 1}
        items['book'] = {'value': 0, 'max': 1}
        items['sword'] = {'value': 0, 'max': 4}
        items['shield'] = {'value': 0, 'max': 3}
        items['half_magic'] = {'value': 0, 'max': 1}
        items['aga'] = {'value': 0, 'max': 1}
        return items

    @staticmethod
    def generate_new_dungeon_dict():
        dungeons = dict()
        dungeons['ep'] = {'pendant': 0, 'total_items': 3, 'items_checked': 0, 'completed': False}
        dungeons['dp'] = {'pendant': 0, 'total_items': 2, 'items_checked': 0, 'completed': False}
        dungeons['th'] = {'pendant': 0, 'total_items': 2, 'items_checked': 0, 'completed': False}
        dungeons['pd'] = {'pendant': 0, 'total_items': 5, 'items_checked': 0, 'completed': False}
        dungeons['sp'] = {'pendant': 0, 'total_items': 6, 'items_checked': 0, 'completed': False}
        dungeons['sw'] = {'pendant': 0, 'total_items': 2, 'items_checked': 0, 'completed': False}
        dungeons['tt'] = {'pendant': 0, 'total_items': 4, 'items_checked': 0, 'completed': False}
        dungeons['ip'] = {'pendant': 0, 'total_items': 3, 'items_checked': 0, 'completed': False}
        dungeons['mm'] = {'pendant': 0, 'total_items': 2, 'items_checked': 0, 'completed': False, 'medallion': 0}
        dungeons['tr'] = {'pendant': 0, 'total_items': 5, 'items_checked': 0, 'completed': False, 'medallion': 0}
        return dungeons

    def __init__(self):
        self.items = Inventory.generate_new_item_dict()
        self.dungeons = Inventory.generate_new_dungeon_dict()
        self.current_time = 0
        self.timer_running = False
        self.light_world_checked = []
        self.dark_world_checked = []

    def increment(self, item_name):
        if item_name in self.items.keys():
            self.items[item_name]['value'] += 1
            if self.items[item_name]['value'] > self.items[item_name]['max']:
                self.items[item_name]['value'] = 0
        elif item_name[:2] in self.dungeons.keys():
            if len(item_name) == 2:
                self.dungeons[item_name]['completed'] = not self.dungeons[item_name]['completed']
            elif 'chest' in item_name:
                self.dungeons[item_name[:2]]['items_checked'] += 1
                if self.dungeons[item_name[:2]]['items_checked'] > self.dungeons[item_name[:2]]['total_items']:
                    self.dungeons[item_name[:2]]['items_checked'] = 0
            elif 'pendant' in item_name:
                self.dungeons[item_name[:2]]['pendant'] += 1
                if self.dungeons[item_name[:2]]['pendant'] > 4:
                    self.dungeons[item_name[:2]]['pendant'] = 0
            elif 'medallion' in item_name and item_name[:2] in ['mm', 'tr']:
                self.dungeons[item_name[:2]]['medallion'] += 1
                if self.dungeons[item_name[:2]]['medallion'] > 3:
                    self.dungeons[item_name[:2]]['medallion'] = 0
            else:
                assert 'completed' in item_name, 'increment(): Invalid item name given.'
                self.dungeons[item_name[:2]]['completed'] = not self.dungeons[item_name[:2]]['completed']

    def decrement(self, item_name):
        if item_name in self.items.keys():
            self.items[item_name]['value'] -= 1
            if self.items[item_name]['value'] < 0:
                self.items[item_name]['value'] = self.items[item_name]['max']
        elif item_name[:2] in self.dungeons.keys():
            if len(item_name) == 2:
                self.dungeons[item_name]['completed'] = not self.dungeons[item_name]['completed']
            elif 'chest' in item_name:
                self.dungeons[item_name[:2]]['items_checked'] -= 1
                if self.dungeons[item_name[:2]]['items_checked'] < 0:
                    self.dungeons[item_name[:2]]['items_checked'] = self.dungeons[item_name[:2]]['total_items']
            elif 'pendant' in item_name:
                self.dungeons[item_name[:2]]['pendant'] -= 1
                if self.dungeons[item_name[:2]]['pendant'] < 0:
                    self.dungeons[item_name[:2]]['pendant'] = 4
            elif 'medallion' in item_name and item_name[:2] in ['mm', 'tr']:
                self.dungeons[item_name[:2]]['medallion'] -= 1
                if self.dungeons[item_name[:2]]['medallion'] < 0:
                    self.dungeons[item_name[:2]]['medallion'] = 3
            else:
                assert 'completed' in item_name, 'increment(): Invalid item name given.'
                self.dungeons[item_name[:2]]['completed'] = not self.dungeons[item_name[:2]]['completed']

    def dark_world_access(self):
        items = self.item_dict()
        dark_world_areas = dict()
        # initial area checks
        dark_world_areas['north'] = items['gloves'] >= 2 or (self.has('gloves') and self.has('hammer'))
        dark_world_areas['south'] = dark_world_areas['north'] or (bool(items['hammer']) and bool(items['gloves']))
        dark_world_areas['east'] = bool(items['aga']) or (bool(items['hammer']) and bool(items['gloves']))
        dark_world_areas['dm_west'] = bool(items['flute']) or (bool(items['gloves']) and bool(items['lantern']))
        dark_world_areas['dm_east'] = dark_world_areas['dm_west'] and \
            (bool(items['mirror']) or (bool(items['hookshot']) and items['gloves'] >= 2))
        dark_world_areas['t_rock'] = dark_world_areas['dm_east'] and items['gloves'] >= 2 and bool(items['hammer'])
        dark_world_areas['mire'] = bool(items['flute']) and items['gloves'] >= 2
        dark_world_areas['ice'] = bool(items['flippers']) and bool(items['gloves'])
        # alternate pathways checks
        prev_check = copy.deepcopy(dark_world_areas)
        next_check = dict()
        while prev_check != next_check:
            next_check = copy.deepcopy(prev_check)
            if prev_check['east'] and bool(items['hookshot']) and (bool(items['hammer']) or bool(items['gloves'])):
                next_check['north'] = True
            if prev_check['south'] and items['gloves'] >= 2:
                next_check['north'] = True
            if prev_check['east'] and items['hammer']:
                next_check['south'] = True
            if prev_check['south'] and items['hammer']:
                next_check['east'] = True
        dark_world_areas = next_check
        dark_world_areas['northeast'] = bool(items['gloves']) and \
            (dark_world_areas['east'] or (dark_world_areas['north'] and bool(items['flippers'])))
        return dark_world_areas

    def item_dict(self):
        return {item_name: item_info['value'] for (item_name, item_info) in self.items.iteritems()}
    
    def has(self, item_name):
        assert item_name in self.items.keys(), 'Inventory.has(): invalid item name given'
        return bool(self.items[item_name]['value'])
    
    def medallions(self):
        has_medallions = {'mm': False, 'tr': False}
        medallion_names = {1: 'bombos', 2: 'ether', 3: 'quake'}
        for dungeon in has_medallions.keys():
            medallion_count = self.dungeons[dungeon]['medallion']
            if medallion_count > 0:
                medallion_name = medallion_names[medallion_count]
                if self.has(medallion_name):
                    has_medallions[dungeon] = True
        return has_medallions

    def pendants(self):
        pendants = {'green': 0, 'other': 0}
        for _, dungeon in self.dungeons.iteritems():
            if dungeon['completed']:
                if dungeon['pendant'] == 1:
                    pendants['green'] += 1
                elif dungeon['pendant'] == 2:
                    pendants['other'] += 1
        return pendants

    def red_crystals(self):
        count = 0
        for _, dungeon in self.dungeons.iteritems():
            if dungeon['completed']:
                if dungeon['pendant'] == 4:
                    count += 1
        return count >= 2

    def dungeon_availability(self):
        dark = self.dark_world_access()
        locs = dict()
        maybes = list()
        locs['ep_access'] = True
        locs['ep_complete'] = locs['ep_access'] and self.has('bow')
        locs['dp_access'] = self.has('book') or (dark['mire'] and self.has('mirror'))
        locs['dp_complete'] = locs['dp_access'] and (self.has('lantern') or self.has('fire_rod')) and self.has('gloves')
        if locs['dp_complete'] and not self.has('boots'):
            maybes.append('dp_complete')
        locs['th_access'] = dark['dm_west'] and (self.has('mirror') or (self.has('hookshot') and self.has('hammer')))
        locs['th_complete'] = locs['th_access']
        if locs['th_complete'] and not self.has('lantern') and not self.has('fire_rod'):
            maybes.append('th_access')
        locs['pd_access'] = dark['east'] and self.has('moon_pearl')
        locs['pd_complete'] = locs['pd_access'] and self.has('bow') and self.has('hammer')
        locs['sp_access'] = dark['south'] and self.has('mirror') and self.has('flippers') and self.has('moon_pearl')
        locs['sp_complete'] = locs['sp_access'] and self.has('hookshot')
        locs['sw_access'] = dark['north'] and self.has('moon_pearl')
        locs['sw_complete'] = locs['sw_access'] and self.has('fire_rod') and self.has('sword')
        locs['tt_access'] = dark['north'] and self.has('moon_pearl')
        locs['tt_complete'] = locs['tt_access']
        locs['ip_access'] = dark['ice'] and (self.has('fire_rod') or self.has('bombos')) and self.has('moon_pearl')
        locs['ip_complete'] = locs['ip_access']
        medallions = self.medallions()
        locs['mm_access'] = dark['mire'] and medallions['mm'] and (self.has('boots') or self.has('hookshot')) and self.has('moon_pearl')
        if self.dungeons['mm']['medallion'] == 0 and dark['mire'] and (self.has('boots') or self.has('hookshot')) and self.has('moon_pearl'):
            maybes.append('mm_access')
        locs['mm_complete'] = locs['mm_access'] and self.has('somaria')
        locs['tr_access'] = dark['t_rock'] and medallions['tr'] and self.has('somaria') and self.has('moon_pearl')
        if self.dungeons['tr']['medallion'] == 0 and dark['t_rock'] and self.has('somaria') and self.has('moon_pearl'):
            maybes.append('tr_access')
        locs['tr_complete'] = locs['tr_access'] and self.has('fire_rod') and self.has('ice_rod')
        return locs, maybes

    def light_world_location_availability(self):
        items = self.item_dict()
        dark = self.dark_world_access()
        pendants = self.pendants()
        locs = dict()
        visible = list()
        dungeons, _ = self.dungeon_availability()
        # SPHERE ZERO
        locs['links_house'] = True
        locs['sanctuary'] = True
        locs['uncle_tunnel'] = True
        locs['escape_front'] = True
        locs['stump_ledge'] = True
        locs['mushroom_spot'] = True
        locs['blinds_house'] = True
        locs['kakariko_well'] = True
        locs['bottle_vendor'] = True
        locs['chicken_house'] = True
        locs['tavern'] = True
        locs['hedge_race'] = True
        locs['aginahs_cave'] = True
        locs['dam'] = True
        locs['mini_moldorm_cave'] = True
        locs['ice_rod_cave'] = True
        locs['sahasrahlas_hut'] = True
        # LOCATIONS WITH REQUIREMENTS
        locs['escape_back'] = self.has('gloves')
        locs['escape_dark'] = self.has('fire_rod')
        locs['graveyard_ledge'] = self.has('mirror') and dark['north']
        locs['kings_tomb'] = self.has('boots') and (items['gloves'] >=2 or (self.has('mirror') and dark['north']))
        locs['witchs_hut'] = self.has('mushroom')
        locs['waterfall_fairy'] = self.has('flippers')
        locs['king_zora'] = self.has('flippers') or self.has('gloves')
        locs['zora_ledge'] = self.has('flippers')
        if not locs['zora_ledge'] and self.has('gloves'):
            visible.append('zora_ledge')
        locs['sahasrahla'] = bool(pendants['green'])
        locs['lake_hylia_island'] = dark['south'] and self.has('flippers') and self.has('mirror')
        if not locs['lake_hylia_island'] and self.has('flippers'):
            visible.append('lake_hylia_island')
        locs['hobo'] = self.has('flippers')
        locs['desert_thief'] = items['gloves'] >= 2 and dark['north'] # TECHNICALLY ALSO REQUIRES BLACKSMITHS
        locs['bombos_tablet'] = self.has('book') and self.has('mirror') and items['sword'] >= 2 and dark['south']
        locs['desert_ledge'] = self.has('book') or (self.has('mirror') and dark['mire'])
        if not locs['desert_ledge']:
            visible.append('desert_ledge')
        locs['checkerboard_cave'] = dark['mire'] and self.has('mirror')
        locs['forest_grove'] = self.has('shovel')
        locs['south_of_grove_cave'] = dark['south'] and self.has('mirror')
        locs['library'] = self.has('boots')
        if not locs['library']:
            visible.append('library')
        locs['magic_bat'] = self.has('powder') and \
            (self.has('hammer') or (dark['north'] and items['gloves'] >= 2 and self.has('mirror')))
        locs['sick_kid'] = self.has('bottles')
        locs['bonk_rocks'] = self.has('boots')
        locs['lumberjack_cave'] = self.has('aga') and self.has('boots')
        if not locs['lumberjack_cave']:
            visible.append('lumberjack_cave')
        locs['pedestal'] = bool(pendants['green']) and pendants['other'] >= 2
        locs['old_man'] = self.has('lantern') and dark['dm_west']
        locs['spectacle_rock'] = dark['dm_west'] and self.has('mirror')
        if not locs['spectacle_rock'] and dark['dm_west']:
            visible.append('spectacle_rock')
        locs['spectacle_rock_cave'] = dark['dm_west']
        locs['ether_tablet'] = self.has('book') and items['sword'] >= 2 and dungeons['th_access']
        locs['paradox_cave'] = dark['dm_west'] and (self.has('hookshot') or (self.has('mirror') and self.has('hammer')))
        locs['spiral_cave'] = locs['paradox_cave']
        locs['mimic_cave'] = dungeons['tr_access'] and self.has('mirror')
        locs['floating_island'] = dark['dm_east'] and self.has('mirror') and self.has('moon_pearl')
        locs['blacksmiths'] = dark['north'] and items['gloves'] >= 2
        return locs, visible

    def dark_world_location_availability(self):
        items = self.item_dict()
        dark = self.dark_world_access()
        locs = dict()
        visible = list()
        locs['pyramid_fairy'] = self.has('moon_pearl') and dark['south'] and self.red_crystals() and \
            (self.has('hammer') or (self.has('aga') and self.has('mirror')))
        locs['pyramid_ledge'] = dark['east']
        locs['catfish'] = dark['east'] and self.has('gloves') and self.has('moon_pearl')
        locs['swamp_cave'] = dark['south'] and self.has('moon_pearl')
        locs['mire_shed'] = dark['mire'] and self.has('moon_pearl')
        locs['haunted_grove'] = dark['south'] and self.has('moon_pearl')
        locs['digging_game'] = dark['south'] and self.has('moon_pearl')
        locs['peg_cave'] = dark['north'] and self.has('hammer') and items['gloves'] >=2 and self.has('moon_pearl')
        locs['doorless_hut'] = dark['north'] and self.has('moon_pearl')
        locs['c_house'] = dark['north'] and self.has('moon_pearl')
        locs['chest_game'] = dark['north'] and self.has('moon_pearl')
        locs['bumper_cave'] = dark['north'] and self.has('cape') and self.has('moon_pearl')
        if not locs['bumper_cave'] and dark['north']:
            visible.append('bumper_cave')
        locs['spike_cave'] = dark['dm_west'] and self.has('hammer') and self.has('moon_pearl') and (self.has('byrna') or self.has('cape'))
        locs['super_bunny_cave'] = dark['dm_east']
        locs['hookshot_cave_front'] = dark['dm_east'] and (self.has('hookshot') or self.has('boots')) and self.has('moon_pearl')
        locs['hookshot_cave_back'] = dark['dm_east'] and self.has('hookshot') and self.has('moon_pearl')
        return locs, visible

    def toggle_timer(self):
        self.timer_running = not self.timer_running

    def display_time(self):
        microseconds = (self.current_time / 10) % 100
        seconds = (self.current_time / 1000) % 60
        minutes = (self.current_time / (1000 * 60)) % 60
        hours = self.current_time / (1000 * 60 * 60)
        if hours > 0:
            return '{:d}:{:02d}:{:02d}.{:02d}'.format(hours, minutes, seconds, microseconds)
        else:
            return '{:02d}:{:02d}.{:02d}'.format(minutes, seconds, microseconds)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    tracker = Inventory()
    item_bg = pygame.image.load(os.path.join('gfx', 'item_bg32.png')).convert()
    item_bg.set_colorkey(ALPHA_COLOR)
    dungeon_bg = pygame.image.load(os.path.join('gfx', 'boss_bg.png')).convert()
    dungeon_bg.set_colorkey(ALPHA_COLOR)
    chest_bg = pygame.image.load(os.path.join('gfx', 'chests', 'chest_bg.png')).convert()
    chest_bg.set_colorkey(ALPHA_COLOR)
    light_world_bg = pygame.image.load(os.path.join('gfx', 'light_world_map.png')).convert()
    dark_world_bg = pygame.image.load(os.path.join('gfx', 'dark_world_map.png')).convert()
    while True:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_handler(event.pos, event.button, tracker)
        # timer
        if tracker.timer_running:
            tracker.current_time += clock.get_rawtime()
        # drawing
        screen.fill(BG_COLOR)
        draw_items(screen, item_bg, tracker.item_dict())
        draw_dungeons(screen, dungeon_bg, tracker)
        draw_dungeon_items(screen, chest_bg, tracker)
        draw_light_world(screen, light_world_bg, tracker)
        draw_dark_world(screen, dark_world_bg, tracker)
        # update
        pygame.display.update()
        clock.tick(FPS)


def click_handler(click_coords, click_button, inventory):
    item_pane = pygame.Rect(DRAW_COORDS['item_bg'], (10 * TILE_SIZE, 3 * TILE_SIZE))
    dungeon_pane = pygame.Rect(DRAW_COORDS['dungeons'], (10 * TILE_SIZE, TILE_SIZE))
    chest_pane = pygame.Rect(DRAW_COORDS['chests'], (10 * TILE_SIZE, TILE_SIZE))
    if item_pane.collidepoint(click_coords[0], click_coords[1]):
        item_click_coords = click_coords[0] / TILE_SIZE, click_coords[1] / TILE_SIZE
        for item_name, item_coords in ITEM_PLACEMENT.iteritems():
            if item_coords == item_click_coords:
                item_click_name = item_name
                break
        if click_button == 1:
            inventory.increment(item_click_name)
        elif click_button == 3:
            inventory.decrement(item_click_name)
    elif dungeon_pane.collidepoint(click_coords[0], click_coords[1]):
        dungeon_click_coords = click_coords[0] - DRAW_COORDS['dungeons'][0], click_coords[1] - DRAW_COORDS['dungeons'][1]
        dungeon_number = (dungeon_click_coords[0] - DRAW_COORDS['dungeons'][0]) / TILE_SIZE
        if dungeon_click_coords[0] % TILE_SIZE <= TILE_SIZE / 2 and dungeon_click_coords[1] % TILE_SIZE > TILE_SIZE / 2:
            if click_button == 1:
                inventory.increment('{}_pendant'.format(DUNGEON_ORDER[dungeon_number]))
            elif click_button == 3:
                inventory.decrement('{}_pendant'.format(DUNGEON_ORDER[dungeon_number]))
        elif DUNGEON_ORDER[dungeon_number] in ['mm', 'tr'] and dungeon_click_coords[0] % TILE_SIZE > TILE_SIZE / 2 and dungeon_click_coords[1] % TILE_SIZE > TILE_SIZE / 2:
            if click_button == 1:
                inventory.increment('{}_medallion'.format(DUNGEON_ORDER[dungeon_number]))
            elif click_button == 3:
                inventory.decrement('{}_medallion'.format(DUNGEON_ORDER[dungeon_number]))
        else:
            inventory.increment(DUNGEON_ORDER[dungeon_number])
    elif chest_pane.collidepoint(click_coords[0], click_coords[1]):
        dungeon_number = (click_coords[0] - DRAW_COORDS['chests'][0]) / TILE_SIZE
        if click_button == 1:
            inventory.increment('{}_chest'.format(DUNGEON_ORDER[dungeon_number]))
        elif click_button == 3:
            inventory.decrement('{}_chest'.format(DUNGEON_ORDER[dungeon_number]))
    else:
        click_found = False
        for location_name, lw_coords in LIGHT_LOCATION_COORDS.iteritems():
            location_rect = pygame.Rect(lw_coords[0] - LOCATION_BORDER, lw_coords[1] - LOCATION_BORDER, LOCATION_BORDER + LOCATION_SIZE, LOCATION_BORDER + LOCATION_SIZE)
            location_rect.left += DRAW_COORDS['light_map'][0]
            location_rect.top += DRAW_COORDS['light_map'][1]
            if location_rect.collidepoint(click_coords):
                if location_name in inventory.light_world_checked:
                    inventory.light_world_checked.remove(location_name)
                else:
                    inventory.light_world_checked.append(location_name)
                click_found = True
                break
        if not click_found:
            for location_name, dw_coords in DARK_LOCATION_COORDS.iteritems():
                location_rect = pygame.Rect(dw_coords[0] - LOCATION_BORDER, dw_coords[1] - LOCATION_BORDER, LOCATION_BORDER + LOCATION_SIZE, LOCATION_BORDER + LOCATION_SIZE)
                location_rect.left += DRAW_COORDS['dark_map'][0]
                location_rect.top += DRAW_COORDS['dark_map'][1]
                if location_rect.collidepoint(click_coords):
                    if location_name in inventory.dark_world_checked:
                        inventory.dark_world_checked.remove(location_name)
                    else:
                        inventory.dark_world_checked.append(location_name)
                    break


def draw_items(draw_surface, item_bg_image, item_dict):
    draw_surface.blit(item_bg_image, DRAW_COORDS['item_bg'])
    shade_square = pygame.Surface((TILE_SIZE, TILE_SIZE))
    shade_square.fill(BG_COLOR)
    shade_square.set_alpha(SHADE_AMOUNT)
    blank_square = pygame.Surface((TILE_SIZE, TILE_SIZE))
    blank_square.fill(BG_COLOR)
    for item_name, item_coords in ITEM_PLACEMENT.iteritems():
        item_draw_coords = TILE_SIZE * item_coords[0] + DRAW_COORDS['item_bg'][0], TILE_SIZE * item_coords[1] + DRAW_COORDS['item_bg'][1]
        if item_dict[item_name] == 0 and item_name != 'mail':
            draw_surface.blit(shade_square, item_draw_coords)
        elif item_dict[item_name] > 1 or (item_dict[item_name] == 1 and item_name in ['boomerang', 'mail', 'bottles', 'aga']):
            draw_surface.blit(blank_square, item_draw_coords)
            upgrade_file = os.path.join('gfx', '{}_{}.png'.format(item_name, item_dict[item_name]))
            upgrade_image = pygame.image.load(upgrade_file).convert()
            upgrade_image.set_colorkey(ALPHA_COLOR)
            draw_surface.blit(upgrade_image, item_draw_coords)


def draw_dungeons(draw_surface, dungeon_bg_image, inventory):
    draw_surface.blit(dungeon_bg_image, DRAW_COORDS['dungeons'])
    shade_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    shade_surface.fill(BG_COLOR)
    shade_surface.set_alpha(SHADE_AMOUNT)
    dungeon_count = 0
    for dungeon_name in DUNGEON_ORDER:
        # shading non-completed dungeons
        if not inventory.dungeons[dungeon_name]['completed']:
            draw_coords = DRAW_COORDS['dungeons'][0] + dungeon_count * TILE_SIZE, DRAW_COORDS['dungeons'][1]
            draw_surface.blit(shade_surface, draw_coords)
        # pendant/crystal images
        if inventory.dungeons[dungeon_name]['pendant'] > 0:
            pendant_coords = draw_coords[0], draw_coords[1] + TILE_SIZE / 2
            image_names = {1: 'pendant_green', 2: 'pendant_other', 3: 'crystal_blue', 4: 'crystal_red'}
            pendant_file = os.path.join('gfx', '{}.png'.format(image_names[inventory.dungeons[dungeon_name]['pendant']]))
            pendant_image = pygame.image.load(pendant_file).convert()
            pendant_image.set_colorkey(ALPHA_COLOR)
            draw_surface.blit(pendant_image, pendant_coords)
        if dungeon_name in ['mm', 'tr'] and inventory.dungeons[dungeon_name]['medallion'] > 0:
            medallion_coords = draw_coords[0] + TILE_SIZE / 2, draw_coords[1] + TILE_SIZE / 2
            medallion_file = os.path.join('gfx', 'medallion_{}.png'.format(inventory.dungeons[dungeon_name]['medallion']))
            medallion_image = pygame.image.load(medallion_file).convert()
            medallion_image.set_colorkey(ALPHA_COLOR)
            draw_surface.blit(medallion_image, medallion_coords)
        dungeon_count += 1


def draw_dungeon_items(draw_surface, chest_bg_image, inventory):
    draw_surface.blit(chest_bg_image, (0, 4 * TILE_SIZE))
    dungeon_count = 0
    for dungeon_name in DUNGEON_ORDER:
        chests_checked = inventory.dungeons[dungeon_name]['items_checked']
        if chests_checked > 0:
            chests_total = inventory.dungeons[dungeon_name]['total_items']
            draw_coords = dungeon_count * TILE_SIZE, 4 * TILE_SIZE
            chest_file = os.path.join('gfx', 'chests', 'chest_{}_{}.png'.format(chests_total, chests_checked))
            chest_image = pygame.image.load(chest_file).convert()
            chest_image.set_colorkey(ALPHA_COLOR)
            draw_surface.blit(chest_image, draw_coords)
        dungeon_count += 1


def draw_light_world(draw_surface, light_world_bg_image, inventory):
    draw_surface.blit(light_world_bg_image, DRAW_COORDS['light_map'])
    lw_locations, lw_visible = inventory.light_world_location_availability()
    # item locations
    for location_name, location_coords in LIGHT_LOCATION_COORDS.iteritems():
        if location_name in inventory.light_world_checked:
            draw_color = CHECKED_COLOR
        elif lw_locations[location_name]:
            draw_color = AVAILABLE_COLOR
        elif location_name in lw_visible:
            draw_color = VISIBLE_COLOR
        else:
            draw_color = UNAVAILABLE_COLOR
        rect_coords = location_coords[0] + DRAW_COORDS['light_map'][0], location_coords[1] + DRAW_COORDS['light_map'][1]
        border_rect = pygame.Rect((0, 0), (2 * LOCATION_BORDER + LOCATION_SIZE, 2 * LOCATION_BORDER + LOCATION_SIZE))
        inner_rect = pygame.Rect((0, 0), (LOCATION_SIZE, LOCATION_SIZE))
        border_rect.center = rect_coords
        inner_rect.center = rect_coords
        pygame.draw.rect(draw_surface, BG_COLOR, border_rect)
        pygame.draw.rect(draw_surface, draw_color, inner_rect)
    # dungeon locations
    dungeon_availability, dungeon_maybes = inventory.dungeon_availability()
    for dungeon_name, dungeon_coords in LIGHT_DUNGEON_COORDS.iteritems():
        draw_coords = LIGHT_DUNGEON_COORDS[dungeon_name][0] + DRAW_COORDS['light_map'][0], LIGHT_DUNGEON_COORDS[dungeon_name][1] + DRAW_COORDS['light_map'][1]
        border_rect = pygame.Rect(0, 0, DUNGEON_SIZE + 2 * DUNGEON_BORDER, DUNGEON_SIZE + 2 * DUNGEON_BORDER)
        border_rect.center = draw_coords
        pygame.draw.rect(draw_surface, BG_COLOR, border_rect)
        outer_rect = pygame.Rect(0, 0, DUNGEON_SIZE, DUNGEON_SIZE)
        outer_rect.center = draw_coords
        if inventory.dungeons[dungeon_name]['items_checked'] == inventory.dungeons[dungeon_name]['total_items']:
            outer_color = CHECKED_COLOR
        elif '{}_access'.format(dungeon_name) in dungeon_maybes:
            outer_color = VISIBLE_COLOR
        elif dungeon_availability['{}_access'.format(dungeon_name)]:
            outer_color = AVAILABLE_COLOR
        else:
            outer_color = UNAVAILABLE_COLOR
        pygame.draw.rect(draw_surface, outer_color, outer_rect)
        inner_rect = pygame.Rect(0, 0, DUNGEON_INNER_SIZE, DUNGEON_INNER_SIZE)
        inner_rect.center = draw_coords
        if inventory.dungeons[dungeon_name]['completed']:
                inner_color = CHECKED_COLOR
        elif dungeon_availability['{}_complete'.format(dungeon_name)]:
            if '{}_complete'.format(dungeon_name) in dungeon_maybes:
                inner_color = VISIBLE_COLOR
            else:
                inner_color = AVAILABLE_COLOR
        else:
            inner_color = UNAVAILABLE_COLOR
        pygame.draw.rect(draw_surface, inner_color, inner_rect)
        boss_rect = pygame.Rect(0, 0, TILE_SIZE / 2, TILE_SIZE / 2)
        boss_rect.center = draw_coords
        boss_file = os.path.join('gfx', 'bosses', 'boss_{}.png'.format(DUNGEON_ORDER.index(dungeon_name)))
        boss_image = pygame.image.load(boss_file).convert()
        boss_scale_image = pygame.transform.scale(boss_image, (TILE_SIZE / 2, TILE_SIZE / 2))
        boss_scale_image.set_colorkey(ALPHA_COLOR)
        draw_surface.blit(boss_scale_image, boss_rect)


def draw_dark_world(draw_surface, dark_world_bg_image, inventory):
    draw_surface.blit(dark_world_bg_image, DRAW_COORDS['dark_map'])
    dw_locations, dw_visible = inventory.dark_world_location_availability()
    # item locations
    for location_name, location_coords in DARK_LOCATION_COORDS.iteritems():
        if location_name in inventory.dark_world_checked:
            draw_color = CHECKED_COLOR
        elif dw_locations[location_name]:
            draw_color = AVAILABLE_COLOR
        elif location_name in dw_visible:
            draw_color = VISIBLE_COLOR
        else:
            draw_color = UNAVAILABLE_COLOR
        rect_coords = location_coords[0] + DRAW_COORDS['dark_map'][0], location_coords[1] + DRAW_COORDS['dark_map'][1]
        border_rect = pygame.Rect((0, 0), (LOCATION_BORDER + LOCATION_SIZE, LOCATION_BORDER + LOCATION_SIZE))
        inner_rect = pygame.Rect((0, 0), (LOCATION_SIZE, LOCATION_SIZE))
        border_rect.center = rect_coords
        inner_rect.center = rect_coords
        pygame.draw.rect(draw_surface, BG_COLOR, border_rect)
        pygame.draw.rect(draw_surface, draw_color, inner_rect)
    # dungeon locations
    dungeon_availability, dungeon_maybes = inventory.dungeon_availability()
    for dungeon_name, dungeon_coords in DARK_DUNGEON_COORDS.iteritems():
        draw_coords = DARK_DUNGEON_COORDS[dungeon_name][0] + DRAW_COORDS['dark_map'][0], DARK_DUNGEON_COORDS[dungeon_name][1] + DRAW_COORDS['dark_map'][1]
        border_rect = pygame.Rect(0, 0, DUNGEON_SIZE + 2 * DUNGEON_BORDER, DUNGEON_SIZE + 2 * DUNGEON_BORDER)
        border_rect.center = draw_coords
        pygame.draw.rect(draw_surface, BG_COLOR, border_rect)
        outer_rect = pygame.Rect(0, 0, DUNGEON_SIZE, DUNGEON_SIZE)
        outer_rect.center = draw_coords
        if inventory.dungeons[dungeon_name]['items_checked'] == inventory.dungeons[dungeon_name]['total_items']:
            outer_color = CHECKED_COLOR
        elif '{}_access'.format(dungeon_name) in dungeon_maybes:
            outer_color = VISIBLE_COLOR
        elif dungeon_availability['{}_access'.format(dungeon_name)]:
            outer_color = AVAILABLE_COLOR
        else:
            outer_color = UNAVAILABLE_COLOR
        pygame.draw.rect(draw_surface, outer_color, outer_rect)
        inner_rect = pygame.Rect(0, 0, DUNGEON_INNER_SIZE, DUNGEON_INNER_SIZE)
        inner_rect.center = draw_coords
        if inventory.dungeons[dungeon_name]['completed']:
                inner_color = CHECKED_COLOR
        elif dungeon_availability['{}_complete'.format(dungeon_name)]:
            if '{}_complete'.format(dungeon_name) in dungeon_maybes:
                inner_color = VISIBLE_COLOR
            else:
                inner_color = AVAILABLE_COLOR
        else:
            inner_color = UNAVAILABLE_COLOR
        pygame.draw.rect(draw_surface, inner_color, inner_rect)
        boss_rect = pygame.Rect(0, 0, TILE_SIZE / 2, TILE_SIZE / 2)
        boss_rect.center = draw_coords
        boss_file = os.path.join('gfx', 'bosses', 'boss_{}.png'.format(DUNGEON_ORDER.index(dungeon_name)))
        boss_image = pygame.image.load(boss_file).convert()
        boss_scale_image = pygame.transform.scale(boss_image, (TILE_SIZE / 2, TILE_SIZE / 2))
        boss_scale_image.set_colorkey(ALPHA_COLOR)
        draw_surface.blit(boss_scale_image, boss_rect)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
