#!/usr/bin/env python

# descriptors from http://www.winning-homebrew.com/beer-flavor-descriptors.html
aroma_basic = [
    'malty', 'grainy', 'sweet',
    'corn', 'hay', 'straw',
    'cracker', 'bicuity',
    'caramel', 'toast', 'roast',
    'coffee', 'espresso', 'burnt',
    'alcohol', 'tobacco', 'gunpowder',
    'leather', 'pine', 'grass',
    'dank', 'piney', 'floral',
    'perfume'
]
aroma_dark_fruit = [
    'raisins', 'currant', 'plum',
    'dates', 'prunes', 'figs',
    'blackberry', 'blueberry'
]
aroma_light_fruit = [
    'banana', 'pineapple', 'apricot',
    'pear', 'apple', 'nectarine',
    'peach', 'mango'
]
aroma_citrus = [
    'lemon', 'lime', 'orange',
    'tangerine', 'clementine',
    'grapefruit', 'grapefruity', 'peel',
    'zest', 'citrus', 'orangey',
]
aroma_other = [
    'metallic', 'vinegar', 'copper',
    'cidery', 'champagne', 'astringent',
    'chlorine'
]
aroma_spices_yeast = [
    'phenolic', 'pepper', 'clove', 'anise',
    'licorice', 'smoke', 'bacon', 'fatty',
    'nutty', 'butterscotch', 'vanilla',
    'earthy', 'woody', 'horsey',
    'bread', 'saddle', 'musty',
    'barnyard', 'spice'
]
appearance_color = [
    'honey', 'caramel', 'red',
    'brown', 'rootbeer', 'amber',
    'chestnut', 'dark', 'apricot',
    'orange', 'black', 'burnt',
    'auburn', 'garnet', 'ruby',
    'copper', 'gold'
]
appearance_clarity = [
    'brilliant', 'hazy', 'cloudy',
    'turbid', 'opaque', 'clear',
    'crystal', 'bright', 'dull',
    'haze'
]
appearance_head = [
    'persistent', 'rocky', 'large',
    'fluffy', 'dissipating', 'lingering',
    'white', 'offwhite', 'tan',
    'frothy', 'delicate'
]
taste_basic = [
    'roasted', 'bready', 'bitter',
    'sweet', 'spicy', 'fruity',
    'chocolate', 'caramel', 'toffee',
    'coffee', 'malty', 'tart',
    'subtle', 'woodsy', 'earthy',
    'sulfur', 'sulfuric'
]
taste_intensity = [
    'assertive', 'mild', 'bold',
    'balanced', 'robust', 'intense',
    'metallic', 'harsh', 'complex',
    'delicate', 'refined', 'hearty'
]
taste_finish = [
    'dry', 'fruity', 'sweet',
    'alcoholic', 'warming', 'bitter',
    'acidic', 'buttery', 'wet',
    'quenching', 'lingering'
]
palate_mouthfeel = [
    'smooth', 'silky', 'velvety',
    'prickly', 'tingly', 'creamy',
    'warming', 'viscous', 'hot',
    'astringent', 'oily'
]
palate_carbonation = [
    'spritzy', 'prickly', 'round',
    'creamy', 'light', 'gassy',
    'sharp', 'delicate'
]
palate_body = [
    'full', 'heavy', 'dense',
    'viscous', 'robust', 'medium',
    'balanced', 'light', 'delicate',
    'wispy'
]
# define larger groups
aroma = (
    aroma_basic + aroma_dark_fruit + aroma_light_fruit +
    aroma_citrus + aroma_other + aroma_spices_yeast
)
appearance = (
    appearance_color + appearance_clarity + appearance_head
)
taste = (
    taste_basic + taste_intensity + taste_finish
)
palate = (
    palate_mouthfeel + palate_carbonation + palate_body
)
# define union of all descriptors
all_descriptors = list(set(
    aroma + appearance + taste + palate
))
