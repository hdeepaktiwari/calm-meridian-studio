"""
Domain Registry - All 20 Specialized Cinematic Domains
Each domain has expert knowledge about its subject matter
"""
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Domain:
    """Base domain class with specialized knowledge"""
    name: str
    icon: str
    description: str
    locations: List[str]
    signature_elements: List[str]
    lighting_conditions: List[str]
    camera_weights: Dict[str, float]
    color_palette: List[str]
    mood_keywords: List[str]
    style_prompt: str

# Domain 1: Ancient Places
ancient_places = Domain(
    name="Ancient Places",
    icon="🏛️",
    description="Historical ruins, ancient temples, and lost civilizations with dramatic architecture and weathered grandeur",
    locations=[
        "Crumbling stone temple", "Ancient amphitheater", "Weathered pyramid",
        "Ruined fortress walls", "Sacred ritual grounds", "Abandoned palace corridors",
        "Ancient marketplace", "Stone carved monuments", "Underground catacombs"
    ],
    signature_elements=[
        "weathered stone columns", "intricate carvings", "moss-covered walls",
        "cracked marble floors", "ancient inscriptions", "stone archways",
        "fallen statues", "overgrown vegetation", "dramatic shadows"
    ],
    lighting_conditions=["golden hour", "dramatic side lighting", "dappled sunlight", "misty morning"],
    camera_weights={"zoom_in": 0.3, "tilt_up": 0.3, "pan_right": 0.2, "zoom_out": 0.15, "pan_left": 0.05},
    color_palette=["warm sandstone", "aged bronze", "weathered grey", "moss green"],
    mood_keywords=["mysterious", "timeless", "majestic", "weathered", "sacred"],
    style_prompt="ancient historical architecture, weathered stone textures, archaeological grandeur"
)

# Domain 2: Modern Mansions
modern_mansions = Domain(
    name="Modern Luxury Mansions",
    icon="🏠",
    description="Contemporary luxury homes with minimalist design, clean lines, and sophisticated interiors",
    locations=[
        "Open concept living room", "Infinity pool terrace", "Modern kitchen",
        "Master bedroom suite", "Home cinema", "Wine cellar",
        "Rooftop lounge", "Spa bathroom", "Smart home office"
    ],
    signature_elements=[
        "floor-to-ceiling windows", "minimalist furniture", "marble countertops",
        "designer lighting fixtures", "indoor plants", "abstract art pieces",
        "sleek appliances", "neutral tones", "geometric patterns"
    ],
    lighting_conditions=["natural daylight", "ambient LED", "warm evening glow", "architectural spotlights"],
    camera_weights={"pan_right": 0.35, "zoom_out": 0.25, "zoom_in": 0.2, "pan_left": 0.15, "tilt_up": 0.05},
    color_palette=["pristine white", "charcoal grey", "warm oak", "matte black"],
    mood_keywords=["sophisticated", "minimalist", "luxurious", "contemporary", "elegant"],
    style_prompt="contemporary luxury interior design, minimalist architecture, high-end residential"
)

# Domain 3: Agricultural Farmhouses
agricultural_farmhouses = Domain(
    name="Lush Agricultural Farmhouses",
    icon="🌾",
    description="Verdant farmland with rustic charm, bountiful crops, and peaceful rural lifestyle",
    locations=[
        "Expansive crop fields", "Rustic farmhouse exterior", "Barn and silos",
        "Vegetable gardens", "Orchard rows", "Farm equipment shed",
        "Country porch", "Grazing pastures", "Farm-to-table kitchen"
    ],
    signature_elements=[
        "rolling green fields", "wooden fences", "hay bales", "farm animals",
        "vintage tractor", "windmill", "crop rows", "wildflowers",
        "rustic wooden barns", "garden vegetables"
    ],
    lighting_conditions=["early morning mist", "bright midday sun", "golden afternoon", "pastoral sunset"],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "pan_left": 0.2, "zoom_in": 0.15, "tilt_up": 0.1},
    color_palette=["vibrant green", "earth brown", "golden wheat", "barn red"],
    mood_keywords=["peaceful", "rustic", "abundant", "pastoral", "wholesome"],
    style_prompt="lush agricultural landscape, rustic farmhouse, verdant countryside"
)

# Domain 4: Ocean & Sea Creatures
ocean_beauty = Domain(
    name="Ocean & Sea Creatures",
    icon="🌊",
    description="Mesmerizing underwater worlds, marine life, and cinematic coastal beauty",
    locations=[
        "Coral reef ecosystem", "Deep ocean depths", "Kelp forest",
        "Rocky coastline", "Tropical beach", "Tide pools",
        "Ocean surface at sunset", "Underwater cave", "Sandy ocean floor"
    ],
    signature_elements=[
        "colorful fish schools", "coral formations", "sea turtles", "dolphins",
        "jellyfish", "waves crashing", "seaweed swaying", "bioluminescence",
        "sun rays through water", "bubbles rising"
    ],
    lighting_conditions=["underwater sunbeams", "blue hour ocean", "golden beach sunset", "bioluminescent glow"],
    camera_weights={"zoom_in": 0.25, "pan_right": 0.25, "zoom_out": 0.2, "pan_left": 0.2, "tilt_up": 0.1},
    color_palette=["deep blue", "turquoise", "coral orange", "sandy beige"],
    mood_keywords=["serene", "mysterious", "vibrant", "flowing", "majestic"],
    style_prompt="underwater cinematography, marine life, oceanic beauty, coastal landscapes"
)

# Domain 5: Lush Green Forests
lush_forests = Domain(
    name="Lush Green Forests",
    icon="🌲",
    description="Dense woodlands with towering trees, nature trails, and rich biodiversity",
    locations=[
        "Ancient forest path", "Canopy from below", "Forest clearing",
        "Moss-covered logs", "Creek through woods", "Fern grotto",
        "Sunlit glade", "Dense undergrowth", "Tree root system"
    ],
    signature_elements=[
        "towering trees", "dappled sunlight", "moss carpets", "ferns",
        "forest mist", "wildlife", "fallen logs", "mushrooms",
        "vines", "leaf litter"
    ],
    lighting_conditions=["dappled forest light", "misty morning", "golden shafts", "overcast soft light"],
    camera_weights={"tilt_up": 0.3, "zoom_in": 0.25, "pan_right": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["forest green", "moss green", "earth brown", "dappled gold"],
    mood_keywords=["tranquil", "primordial", "lush", "mystical", "verdant"],
    style_prompt="dense forest cinematography, woodland atmosphere, rich green vegetation"
)

# Domain 6: Himalayan Beauty
himalayan_beauty = Domain(
    name="Beautiful Himalayas",
    icon="🏔️",
    description="Majestic mountain peaks, serene valleys, and ancient monasteries in the world's highest ranges",
    locations=[
        "Snow-capped peaks", "Mountain monastery", "Alpine meadow",
        "Prayer flag ridge", "Glacial valley", "Mountain village",
        "High altitude lake", "Rocky mountain path", "Panoramic vista"
    ],
    signature_elements=[
        "snow-covered mountains", "prayer flags", "stone stupas",
        "yaks grazing", "terraced fields", "mountain streams",
        "Buddhist monasteries", "pine forests", "dramatic cliffs"
    ],
    lighting_conditions=["crisp mountain light", "golden hour peaks", "misty valleys", "clear blue sky"],
    camera_weights={"zoom_out": 0.3, "pan_right": 0.25, "tilt_up": 0.2, "zoom_in": 0.15, "pan_left": 0.1},
    color_palette=["snow white", "sky blue", "prayer flag colors", "stone grey"],
    mood_keywords=["majestic", "serene", "spiritual", "pristine", "awe-inspiring"],
    style_prompt="Himalayan mountain cinematography, alpine landscapes, spiritual atmosphere"
)

# Domain 7: Lakeside Lifestyle
lakeside_lifestyle = Domain(
    name="Lakeside Lifestyle",
    icon="🏞️",
    description="Tranquil lake houses with boats, BBQ areas, and relaxed waterfront living",
    locations=[
        "Wooden dock", "Lake house porch", "Boat on water",
        "BBQ deck", "Lakeside fire pit", "Hammock between trees",
        "Fishing spot", "Sunset over lake", "Morning mist on water"
    ],
    signature_elements=[
        "wooden boats", "dock chairs", "BBQ grill", "life jackets",
        "fishing rods", "lake reflections", "water lilies",
        "canoes", "campfire", "porch swing"
    ],
    lighting_conditions=["soft morning mist", "midday sparkle", "golden evening", "twilight blues"],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "pan_left": 0.2, "zoom_in": 0.15, "tilt_up": 0.1},
    color_palette=["lake blue", "wooden brown", "sunset orange", "nature green"],
    mood_keywords=["relaxed", "peaceful", "idyllic", "recreational", "cozy"],
    style_prompt="lakeside lifestyle, waterfront living, recreational lake scenes"
)

# Domain 8: Colorful American Roads
colorful_roads = Domain(
    name="Colorful American Roads",
    icon="🛣️",
    description="Scenic highways covered with autumn foliage and vibrant tree canopies",
    locations=[
        "Winding mountain road", "Tree tunnel drive", "Scenic overlook",
        "Country road through forest", "Autumn parkway", "Covered bridge",
        "Road beside stream", "Vista point", "Foliage-lined highway"
    ],
    signature_elements=[
        "colorful autumn leaves", "winding asphalt", "tree canopies",
        "mountain vistas", "fallen leaves", "white road lines",
        "guard rails", "road signs", "distant mountains"
    ],
    lighting_conditions=["golden autumn light", "soft overcast", "sun through trees", "vibrant midday"],
    camera_weights={"pan_right": 0.35, "zoom_in": 0.25, "pan_left": 0.2, "zoom_out": 0.15, "tilt_up": 0.05},
    color_palette=["autumn red", "golden yellow", "orange", "forest green"],
    mood_keywords=["scenic", "colorful", "peaceful", "journey", "autumnal"],
    style_prompt="autumn road cinematography, colorful foliage, scenic highway"
)

# Domain 9: Antarctica Beauty
antarctica = Domain(
    name="Antarctica Beauty",
    icon="🐧",
    description="Pristine polar landscapes with ice formations, wildlife, and extreme beauty",
    locations=[
        "Ice shelf edge", "Penguin colony", "Glacial ice cave",
        "Iceberg field", "Research station", "Seal haul-out",
        "Frozen ocean surface", "Ice cliffs", "Polar plateau"
    ],
    signature_elements=[
        "massive icebergs", "penguin colonies", "blue glacial ice",
        "aurora australis", "seals", "ice formations",
        "snow-covered peaks", "frozen ocean", "research vessels"
    ],
    lighting_conditions=["polar daylight", "blue hour", "aurora glow", "pristine white light"],
    camera_weights={"zoom_out": 0.3, "pan_right": 0.25, "zoom_in": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["ice blue", "pristine white", "aurora green", "deep ocean blue"],
    mood_keywords=["pristine", "extreme", "majestic", "remote", "otherworldly"],
    style_prompt="Antarctic landscape, polar cinematography, glacial ice beauty"
)

# Domain 10: Life in Space
space_life = Domain(
    name="Life in Space",
    icon="🚀",
    description="Cosmic beauty with planets, nebulae, space stations, and celestial wonders",
    locations=[
        "International Space Station", "Nebula field", "Planetary surface",
        "Asteroid belt", "Deep space vista", "Space station interior",
        "Lunar landscape", "Mars terrain", "Starfield"
    ],
    signature_elements=[
        "stars", "planets", "nebulae", "space station modules",
        "satellites", "cosmic dust", "galaxies", "asteroids",
        "Earth from space", "zero gravity"
    ],
    lighting_conditions=["starlight", "solar illumination", "nebula glow", "Earth shine"],
    camera_weights={"zoom_in": 0.3, "zoom_out": 0.3, "pan_right": 0.2, "pan_left": 0.15, "tilt_up": 0.05},
    color_palette=["deep space black", "nebula purple", "star white", "planet blue"],
    mood_keywords=["infinite", "cosmic", "awe-inspiring", "mysterious", "vast"],
    style_prompt="space cinematography, cosmic scenes, celestial beauty, astronomical wonders"
)

# Domain 11: Luxury Cruise Ships
luxury_cruise = Domain(
    name="Luxury Cruise Ships",
    icon="🚢",
    description="Opulent cruise ship life with pools, dining, entertainment, and ocean views",
    locations=[
        "Pool deck", "Grand dining hall", "Luxury suite", "Theater",
        "Sky lounge", "Spa", "Casino", "Observation deck",
        "Captain's bridge", "Promenade"
    ],
    signature_elements=[
        "infinity pools", "elegant dining tables", "chandeliers",
        "ocean views", "deck chairs", "champagne", "entertainment stages",
        "luxury cabins", "panoramic windows", "sunset at sea"
    ],
    lighting_conditions=["golden ocean sunset", "elegant interior lighting", "poolside glow", "starlit deck"],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "zoom_in": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["ocean blue", "luxury gold", "pristine white", "sunset orange"],
    mood_keywords=["luxurious", "relaxing", "opulent", "elegant", "adventurous"],
    style_prompt="luxury cruise ship, elegant maritime lifestyle, upscale travel"
)

# Domain 12: Luxury Yachts
luxury_yachts = Domain(
    name="Luxury Yachts",
    icon="⛵",
    description="Private yacht lifestyle with exclusivity, ocean adventures, and premium amenities",
    locations=[
        "Yacht deck", "Helm station", "Master cabin", "Lounge area",
        "Sundeck", "Water sports platform", "Dining area", "Jacuzzi",
        "Yacht marina", "Open ocean cruising"
    ],
    signature_elements=[
        "sleek yacht design", "teak decks", "leather seating",
        "water sports equipment", "champagne", "ocean spray",
        "sunset cruising", "luxury interiors", "navigation equipment"
    ],
    lighting_conditions=["bright ocean sun", "golden hour at sea", "yacht interior ambient", "moonlit water"],
    camera_weights={"pan_right": 0.3, "zoom_in": 0.25, "zoom_out": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["yacht white", "ocean blue", "teak brown", "chrome silver"],
    mood_keywords=["exclusive", "luxurious", "adventurous", "prestigious", "free"],
    style_prompt="luxury yacht lifestyle, private maritime, upscale boating"
)

# Domain 13: Desert Life Worldwide
desert_life = Domain(
    name="Desert Life Worldwide",
    icon="🏜️",
    description="Vast desert landscapes from Sahara to Arabian to American deserts with unique beauty",
    locations=[
        "Sand dunes", "Desert oasis", "Canyon walls", "Salt flats",
        "Rock formations", "Desert sunset", "Bedouin camp", "Cactus field",
        "Desert night sky", "Ancient caravan route"
    ],
    signature_elements=[
        "rippled sand", "cacti", "camels", "rock formations",
        "heat shimmer", "desert flora", "sand storms", "oasis palms",
        "star-filled sky", "dramatic shadows"
    ],
    lighting_conditions=["harsh midday sun", "golden hour", "blue hour", "starlit night"],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "tilt_up": 0.2, "zoom_in": 0.15, "pan_left": 0.1},
    color_palette=["golden sand", "desert orange", "sky blue", "earth red"],
    mood_keywords=["vast", "harsh", "serene", "timeless", "dramatic"],
    style_prompt="desert cinematography, arid landscapes, sand dunes, desert life"
)

# Domain 14: Tropical Greenery
tropical_greenery = Domain(
    name="Tropical Greenery (Indonesia, Kerala)",
    icon="🌴",
    description="Lush tropical vegetation with rice terraces, palm trees, and soothing green landscapes",
    locations=[
        "Rice terrace fields", "Tropical waterfall", "Palm grove",
        "Jungle canopy", "Bamboo forest", "Tropical beach",
        "Village in greenery", "River through jungle", "Tea plantations"
    ],
    signature_elements=[
        "terraced rice fields", "coconut palms", "tropical flowers",
        "banana leaves", "waterfalls", "dense vegetation",
        "traditional huts", "tropical birds", "jungle vines"
    ],
    lighting_conditions=["soft tropical light", "monsoon clouds", "dappled jungle sun", "misty morning"],
    camera_weights={"pan_right": 0.3, "zoom_in": 0.25, "zoom_out": 0.2, "tilt_up": 0.15, "pan_left": 0.1},
    color_palette=["vibrant green", "tropical blue", "earth brown", "flower colors"],
    mood_keywords=["lush", "tranquil", "tropical", "verdant", "peaceful"],
    style_prompt="tropical landscape, lush greenery, rice terraces, tropical paradise"
)

# Domain 15: Buddhist Lifestyle
buddhist_lifestyle = Domain(
    name="Buddhist Lifestyle & Temples",
    icon="🕉️",
    description="Tibetan monasteries, temples, prayer flags, and spiritual landscapes across Buddhist regions",
    locations=[
        "Mountain monastery", "Prayer wheel hall", "Temple interior",
        "Meditation cave", "Stupa courtyard", "Monk quarters",
        "Prayer flag ridge", "Buddhist shrine", "Temple garden"
    ],
    signature_elements=[
        "prayer flags", "golden Buddha statues", "prayer wheels",
        "monks in robes", "incense smoke", "mandala art",
        "singing bowls", "butter lamps", "thangka paintings"
    ],
    lighting_conditions=["soft temple light", "golden hour mountains", "candlelit interiors", "misty morning"],
    camera_weights={"tilt_up": 0.3, "zoom_in": 0.25, "pan_right": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["saffron orange", "prayer flag colors", "gold", "temple red"],
    mood_keywords=["spiritual", "peaceful", "sacred", "meditative", "timeless"],
    style_prompt="Buddhist temple cinematography, spiritual atmosphere, Tibetan culture"
)

# Domain 16: Ancient European Cities
ancient_european = Domain(
    name="Ancient European Cities",
    icon="🏰",
    description="Historic European cities with cobblestone streets, medieval architecture, and timeless beauty",
    locations=[
        "Cobblestone plaza", "Medieval castle", "Cathedral interior",
        "Narrow alleyway", "Town square", "Ancient bridge",
        "City walls", "Market street", "Gothic architecture"
    ],
    signature_elements=[
        "cobblestone streets", "Gothic spires", "gas lamps",
        "ivy-covered walls", "cafe terraces", "church bells",
        "medieval towers", "stone bridges", "baroque facades"
    ],
    lighting_conditions=["golden afternoon", "foggy morning", "twilight blue", "warm street lamps"],
    camera_weights={"pan_right": 0.3, "zoom_in": 0.25, "tilt_up": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["aged stone", "terracotta", "slate grey", "warm cream"],
    mood_keywords=["historic", "romantic", "timeless", "charming", "atmospheric"],
    style_prompt="European historic city, medieval architecture, cobblestone streets"
)

# Domain 17: Japanese Beauty
japanese_beauty = Domain(
    name="Japanese Natural & Cultural Beauty",
    icon="🗾",
    description="Classical Japanese buildings, agricultural fields, cherry blossoms, and natural serenity",
    locations=[
        "Cherry blossom grove", "Traditional temple", "Rice paddy fields",
        "Japanese garden", "Bamboo forest", "Tea house",
        "Mount Fuji vista", "Torii gate", "Zen rock garden"
    ],
    signature_elements=[
        "cherry blossoms", "torii gates", "traditional architecture",
        "bonsai trees", "koi ponds", "stone lanterns",
        "tatami rooms", "rice fields", "maple leaves"
    ],
    lighting_conditions=["soft spring light", "golden autumn", "misty morning", "zen garden calm"],
    camera_weights={"pan_right": 0.3, "zoom_in": 0.25, "tilt_up": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["cherry blossom pink", "zen green", "red shrine", "natural wood"],
    mood_keywords=["serene", "harmonious", "peaceful", "elegant", "traditional"],
    style_prompt="Japanese landscape, traditional architecture, natural beauty, zen atmosphere"
)

# Domain 18: Amazon Rainforest
amazon_rainforest = Domain(
    name="Amazon Rainforest Beauty",
    icon="🦜",
    description="Wild jungle beauty with rivers, biodiversity, and untamed natural splendor",
    locations=[
        "River through jungle", "Canopy walkway", "Jungle floor",
        "Waterfall", "Tree roots", "Wildlife habitat",
        "Riverbank", "Dense vegetation", "Ancient trees"
    ],
    signature_elements=[
        "dense canopy", "tropical birds", "river dolphins",
        "exotic flowers", "jungle vines", "massive trees",
        "colorful frogs", "butterflies", "misty atmosphere"
    ],
    lighting_conditions=["dappled jungle light", "early morning mist", "filtered sunbeams", "twilight green"],
    camera_weights={"zoom_in": 0.3, "tilt_up": 0.25, "pan_right": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["jungle green", "tropical blue", "earth brown", "vibrant wildlife colors"],
    mood_keywords=["wild", "mysterious", "vibrant", "primordial", "untamed"],
    style_prompt="Amazon rainforest, jungle cinematography, tropical biodiversity"
)

# Domain 19: Beautiful Beaches
beautiful_beaches = Domain(
    name="Beautiful Beaches Worldwide",
    icon="🏖️",
    description="Stunning coastal paradises with white sand, turquoise water, and tropical beauty",
    locations=[
        "White sand beach", "Palm-lined shore", "Rocky cove",
        "Beach sunset", "Tide pools", "Dunes",
        "Beach resort", "Coastal cliffs", "Tropical lagoon"
    ],
    signature_elements=[
        "white sand", "turquoise water", "palm trees",
        "beach umbrellas", "waves", "seashells",
        "beach chairs", "sunset", "clear water"
    ],
    lighting_conditions=["bright beach sun", "golden sunset", "soft morning", "blue hour"],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "zoom_in": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["turquoise", "white sand", "sunset orange", "sky blue"],
    mood_keywords=["relaxing", "tropical", "paradise", "peaceful", "idyllic"],
    style_prompt="beach cinematography, tropical paradise, coastal beauty"
)

# Domain 20: Luxury Palace Interiors
luxury_palace = Domain(
    name="Luxury Palace Interiors",
    icon="👑",
    description="Opulent royal interiors with grand furnishings, chandeliers, and baroque elegance",
    locations=[
        "Grand ballroom", "Throne room", "Royal library",
        "Music room with piano", "Dining hall", "Game room with snooker",
        "Master bedroom", "Gallery", "Private study"
    ],
    signature_elements=[
        "crystal chandeliers", "grand piano", "velvet sofas",
        "snooker table", "throne chairs", "marble floors",
        "gold accents", "tapestries", "ornate mirrors"
    ],
    lighting_conditions=["golden chandelier glow", "natural window light", "candlelit ambience", "sunset through windows"],
    camera_weights={"zoom_in": 0.3, "pan_right": 0.25, "zoom_out": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["royal gold", "marble white", "velvet red", "ornate bronze"],
    mood_keywords=["opulent", "royal", "majestic", "elegant", "sophisticated"],
    style_prompt="palace interior, royal luxury, baroque architecture, opulent furnishings"
)

# Registry of all domains
DOMAIN_REGISTRY = {
    "Ancient Places": ancient_places,
    "Modern Luxury Mansions": modern_mansions,
    "Lush Agricultural Farmhouses": agricultural_farmhouses,
    "Ocean & Sea Creatures": ocean_beauty,
    "Lush Green Forests": lush_forests,
    "Beautiful Himalayas": himalayan_beauty,
    "Lakeside Lifestyle": lakeside_lifestyle,
    "Colorful American Roads": colorful_roads,
    "Antarctica Beauty": antarctica,
    "Life in Space": space_life,
    "Luxury Cruise Ships": luxury_cruise,
    "Luxury Yachts": luxury_yachts,
    "Desert Life Worldwide": desert_life,
    "Tropical Greenery": tropical_greenery,
    "Buddhist Lifestyle": buddhist_lifestyle,
    "Ancient European Cities": ancient_european,
    "Japanese Beauty": japanese_beauty,
    "Amazon Rainforest": amazon_rainforest,
    "Beautiful Beaches": beautiful_beaches,
    "Luxury Palace Interiors": luxury_palace,
}