def new_items():
    # Items are in a dict as str: int pairs, where the str is the name of the item/upgrade, and the int is the level.
    return {'mail': 0,              # 0-2: green, blue, red
            'sword': 0,             # 0-4: none, fighter's, master, tempered, butter
            'shield': 0,            # 0-3: none, toy, fire, riot
            'gloves': 0,            # 0-2: none, gloves, mitts
            'boots': 0,
            'flippers': 0,
            'moon_pearl': 0,
            'bow': 0,
            'silvers': 0,
            'boomerang_blue': 0,
            'boomerang_red': 0,
            'hookshot': 0,
            'mushroom': 0,
            'powder': 0,
            'fire_rod': 0,
            'ice_rod': 0,
            'bombos': 0,
            'ether': 0,
            'quake': 0,
            'lantern': 0,
            'hammer': 0,
            'shovel': 0,
            'flute': 0,
            'net': 0,
            'book': 0,
            'bottles': 0,           # 0-4: number of bottles
            'cane_somaria': 0,
            'cane_byrna': 0,
            'cape': 0,
            'mirror': 0,
            'aga': 0,
            'green_pendant': 0,
            'other_pendants': 0,
            'red_crystals': 0,
            'blue_crystals': 0,
            'mire_medallion': 0,
            'tr_medallion': 0
            }


def dark_world_access(items):
    dw_points = dict()
    dw_points['castle'] = bool(items['aga'])
    dw_points['lost_woods'] = items['gloves'] >= 2 or (bool(items['hammer']) and bool(items)['gloves'])
    dw_points['east'] = bool(items['gloves']) and bool(items['hammer'])
    dw_points['swamp'] = dw_points['east']
    dw_points['lake'] = bool(items['flippers']) and items['gloves'] >= 2
    dw_points['desert'] = bool(items['flute']) and items['gloves'] >= 2
    dw_points['dm_west'] = bool(items['flute']) or (bool(items['gloves']) and bool(items['lantern']))
    dw_points['dm_east'] = dw_points['dm_west'] and items['gloves'] >= 2 and (bool(items['hookshot']) \
                            or (bool(items['mirror']) and bool(items['hammer'])))
    dw_points['t_rock'] = dw_points['dm_west'] and bool(items['hammer']) and items['gloves'] >= 2 \
                            and (bool(items['hookshot']) or (bool(items['mirror']) and bool(items['hammer'])))
    return dw_points


def light_world_availability(items):
    dw_spots = dark_world_access(items)
    lw_locs = dict()
    lw_locs['links_house'] = True
    lw_locs['uncle_tunnel'] = True
    lw_locs['lumberjack_cave'] = bool(items['aga'])
    lw_locs['lost_woods_ledge'] = True
    lw_locs['mushroom_spot'] = True
    lw_locs['pedestal'] = bool(items['green_pendant']) and items['other_pendants'] >= 2
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
                              ((bool(items['hookshot']) or (bool(items['mirror'])) and bool(items['hammer'])))
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
    lw_locs['sasha'] = bool(items['green_pendant'])
    # TODO -- dungeon #0? (escape + sanctuary)
    return lw_locs


def dark_world_availability(items):
    dw_locs = dict()
    dw_spots = dark_world_access(items)
    '''
    dw_locs[''] =
    bool(items[''])
    '''
    return dw_locs


def main():
    # for testing purposes
    items = new_items()
    lw_locs = light_world_availability(items)
    print 'Item values:'
    for name, value in items.iteritems():
        print '{}: {}'.format(name, value)
    print 'Light World item location availability:'
    print 'Sphere 0 (minus escape):'
    for name, value in lw_locs.iteritems():
        if value:
            print '{}: {}'.format(name, value)
    print 'Initially unavailable locations:'
    for name, value in lw_locs.iteritems():
        if not value:
            print '{}: {}'.format(name, value)


if __name__ == '__main__':
    main()
