"""
Domain Registry - All 20 Specialized Cinematic Domains
Each domain has expert knowledge about its subject matter
"""
from dataclasses import dataclass, field
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
    # New dimension fields with defaults for backward compatibility
    time_periods: List[str] = field(default_factory=list)
    seasons: List[str] = field(default_factory=list)
    weather_conditions: List[str] = field(default_factory=list)
    perspectives: List[str] = field(default_factory=list)
    narrative_themes: List[str] = field(default_factory=list)

# Domain 1: Ancient Places
ancient_places = Domain(
    name="Ancient Places",
    icon="🏛️",
    description="Historical ruins, ancient temples, and lost civilizations with dramatic architecture and weathered grandeur",
    locations=[
        "Crumbling stone temple overgrown with roots", "Ancient amphitheater at dusk",
        "Weathered pyramid half-buried in sand", "Ruined fortress walls above a river gorge",
        "Sacred ritual grounds with standing stones", "Abandoned palace corridors with faded frescoes",
        "Ancient marketplace with worn cobblestones", "Stone carved monuments on a cliff face",
        "Underground catacombs with torch-lit alcoves", "Sunken temple partially submerged in a lake",
        "Hilltop acropolis overlooking olive groves", "Step well descending into darkness",
        "Ruined aqueduct stretching across a valley", "Megalithic stone circle at dawn",
        "Cliff-carved monastery with narrow ledge paths", "Overgrown zigzurat reclaimed by jungle",
        "Ancient astronomical observatory ruins", "Collapsed Roman bathhouse with mosaic floors",
        "Volcanic ruins preserved in ash", "Cave temple with carved pillars",
        "Desert citadel with sand-worn battlements", "Ancient library ruins with scattered stone tablets",
        "Processional avenue lined with sphinx statues", "Terracotta warrior burial chamber",
        "Flooded crypt with reflections on still water", "Ruined lighthouse on a remote headland",
        "Oracle chamber with carved stone seats"
    ],
    signature_elements=[
        "weathered stone columns", "intricate bas-relief carvings", "moss-covered walls",
        "cracked marble floors", "ancient inscriptions in forgotten scripts", "stone archways with keystone detail",
        "fallen headless statues", "overgrown vegetation reclaiming stone", "dramatic shadows through ruins",
        "worn stone steps polished by centuries", "terracotta oil lamps", "ancient water channels",
        "carved deity faces in stone", "root systems splitting masonry", "lichen patterns on granite",
        "bronze age tools embedded in earth", "faded wall paintings", "scattered pottery shards",
        "stone sundial", "sacrificial altar stone", "hieroglyphic panels",
        "petrified wooden beams", "eroded gargoyles", "collapsed dome revealing sky",
        "ancient metal door hinges green with verdigris"
    ],
    lighting_conditions=[
        "golden hour through ruined archways", "dramatic side lighting with long shadows",
        "dappled sunlight through overgrown canopy", "misty morning diffusing ancient silhouettes",
        "torch-lit underground chambers", "moonlight on pale stone",
        "overcast sky lending somber weight", "sunrise hitting only the tallest column"
    ],
    camera_weights={"zoom_in": 0.3, "tilt_up": 0.3, "pan_right": 0.2, "zoom_out": 0.15, "pan_left": 0.05},
    color_palette=["warm sandstone", "aged bronze", "weathered grey", "moss green"],
    mood_keywords=["mysterious", "timeless", "majestic", "weathered", "sacred", "haunting", "solemn", "ancient"],
    style_prompt="ancient historical architecture, weathered stone textures, archaeological grandeur",
    time_periods=[
        "pre-dawn blue light", "first light touching highest stones", "golden hour",
        "harsh noon revealing every crack", "late afternoon amber", "blue hour silhouettes",
        "twilight with first stars", "midnight under full moon", "eclipse shadow",
        "dawn after a storm"
    ],
    seasons=[
        "dry season with cracked earth", "spring wildflowers among ruins", "summer heat shimmer",
        "autumn leaves filling courtyards", "mild winter with frost on stone",
        "monsoon rain streaming down carved faces", "early spring moss growth",
        "late autumn fog clinging to walls"
    ],
    weather_conditions=[
        "light fog weaving through columns", "after rain with wet stone gleaming",
        "approaching storm with dramatic clouds", "clear crisp air with sharp shadows",
        "dust haze from nearby desert", "gentle drizzle on ancient stone",
        "wind carrying sand across floors", "humidity causing stone to sweat",
        "rainbow arcing over ruins"
    ],
    perspectives=[
        "aerial drone revealing full layout", "ground level through fallen columns",
        "macro close-up of carved details", "through a crumbling window frame",
        "reflection in standing water", "looking up from inside a well",
        "from behind overgrown vegetation", "worm's eye view along stone floor",
        "bird's eye directly above", "peering through a narrow doorway"
    ],
    narrative_themes=[
        "civilization lost to time", "nature reclaiming human works", "sacred geometry revealed",
        "echoes of daily life", "the weight of centuries", "forgotten grandeur",
        "archaeological discovery", "spiritual pilgrimage", "the last stones standing",
        "dialogue between ruin and sky"
    ]
)

# Domain 2: Modern Mansions
modern_mansions = Domain(
    name="Modern Luxury Mansions",
    icon="🏠",
    description="Contemporary luxury homes with minimalist design, clean lines, and sophisticated interiors",
    locations=[
        "Open concept living room with double-height ceiling", "Infinity pool terrace overlooking city lights",
        "Chef's kitchen with waterfall island", "Master bedroom suite with panoramic glass wall",
        "Private home cinema with tiered seating", "Temperature-controlled wine cellar",
        "Rooftop lounge with fire pit", "Spa bathroom with rain shower and soaking tub",
        "Smart home office with library wall", "Indoor-outdoor courtyard with mature olive tree",
        "Glass-walled staircase with floating steps", "Underground garage with car turntable",
        "Meditation garden with water feature", "Art gallery hallway with track lighting",
        "Cantilevered balcony over a ravine", "Pool house with retractable glass walls",
        "Walk-in closet with island and chandelier", "Basement entertainment bar with aquarium wall",
        "Outdoor kitchen and dining pavilion", "Japanese-inspired entrance with stone path",
        "Gym with floor-to-ceiling mirrors and city view", "Guest casita with private garden",
        "Koi pond courtyard visible from living room", "Green roof terrace with wildflowers",
        "Library with rolling ladder and reading nook", "Breakfast nook in a glass conservatory"
    ],
    signature_elements=[
        "floor-to-ceiling windows", "minimalist furniture with clean geometry", "marble countertops and backsplashes",
        "designer pendant lighting fixtures", "curated indoor plant arrangements", "large-scale abstract art pieces",
        "sleek integrated appliances", "neutral tones with texture contrast", "geometric patterns in tile and wood",
        "cantilevered concrete overhangs", "water features with LED underlighting", "bespoke millwork and cabinetry",
        "statement fireplace with stone surround", "smart home control panels", "polished concrete floors",
        "custom wine displays", "floating vanity with vessel sink", "retractable glass walls opening to garden",
        "sculptural furniture as focal point", "hidden door to secret room", "green living wall",
        "skylight flooding space with light", "brass and matte black hardware", "terrazzo flooring",
        "infinity edge detail on pool or countertop"
    ],
    lighting_conditions=[
        "natural daylight flooding through glass walls", "ambient LED strip lighting at night",
        "warm evening glow from designer fixtures", "architectural spotlights on art",
        "candlelit dinner atmosphere", "blue hour exterior with interior warmth glowing",
        "morning sun casting long shadows through louvers", "moonlight reflecting off pool into living space"
    ],
    camera_weights={"pan_right": 0.35, "zoom_out": 0.25, "zoom_in": 0.2, "pan_left": 0.15, "tilt_up": 0.05},
    color_palette=["pristine white", "charcoal grey", "warm oak", "matte black"],
    mood_keywords=["sophisticated", "minimalist", "luxurious", "contemporary", "elegant", "serene", "aspirational", "refined"],
    style_prompt="contemporary luxury interior design, minimalist architecture, high-end residential",
    time_periods=[
        "sunrise with first light entering east-facing glass", "mid-morning bright and airy",
        "golden hour warming the facade", "blue hour with interior lights on",
        "late evening ambient mood", "midnight pool glow",
        "overcast midday soft and diffused", "dawn mist around the exterior"
    ],
    seasons=[
        "summer with lush landscaping", "autumn with warm-toned decor accents",
        "winter evening with fireplace lit", "spring with garden in bloom",
        "rainy season with water on glass walls", "dry summer with pool as focal point",
        "holiday season with subtle elegant decor", "early spring cleaning freshness"
    ],
    weather_conditions=[
        "clear day with sharp shadows", "overcast giving soft flat light",
        "rain streaming down glass walls", "fog outside with cozy interior",
        "snow on rooftop terrace", "golden light after afternoon storm",
        "wind rippling pool surface", "humid evening with condensation on glass"
    ],
    perspectives=[
        "aerial drone showing rooftop and pool", "ground level entrance approach",
        "macro close-up of material textures", "through floor-to-ceiling window from outside",
        "reflection in pool surface", "looking up through glass atrium",
        "from courtyard into living space", "symmetrical front elevation",
        "tracking shot through connected rooms", "overhead plan view of living area"
    ],
    narrative_themes=[
        "sanctuary from the world", "architecture as art", "light and shadow play",
        "indoor-outdoor living", "material luxury", "curated minimalism",
        "technology meets comfort", "private paradise", "design intentionality",
        "the quiet of wealth"
    ]
)

# Domain 3: Agricultural Farmhouses
agricultural_farmhouses = Domain(
    name="Lush Agricultural Farmhouses",
    icon="🌾",
    description="Verdant farmland with rustic charm, bountiful crops, and peaceful rural lifestyle",
    locations=[
        "Expansive wheat field at harvest time", "Rustic farmhouse with wraparound porch",
        "Red barn with weathered siding and silos", "Vegetable garden rows in morning dew",
        "Apple orchard in full bloom", "Farm equipment shed with vintage tractor",
        "Country porch with rocking chairs", "Grazing pastures with stone walls",
        "Farm-to-table kitchen with hanging herbs", "Lavender field stretching to horizon",
        "Sunflower maze at golden hour", "Beehive apiaries near wildflower meadow",
        "Greenhouse with tomato vines overhead", "Grain mill beside a stream",
        "Sheep paddock on rolling hills", "Farm pond with ducks and willows",
        "Root cellar with preserved jars", "Vineyard rows on a slope",
        "Corn field with scarecrow silhouette", "Dairy barn interior with hay loft",
        "Herb garden with stone pathways", "Farmstead from hilltop vantage",
        "Irrigation canal between crop rows", "Farmers market stand with harvest display",
        "Hay field with round bales at sunset", "Chicken coop garden with free-range hens",
        "Old stone well in farmyard"
    ],
    signature_elements=[
        "rolling green fields to horizon", "weathered wooden fences", "golden hay bales scattered in field",
        "farm animals grazing peacefully", "vintage tractor with patina", "turning windmill",
        "neat crop rows diminishing in perspective", "wildflowers along fence lines", "rustic wooden barns with gambrel roofs",
        "garden vegetables glistening with dew", "stone farmhouse walls", "hanging dried herbs",
        "milk churns by the door", "wagon wheels leaning on walls", "hand-painted farm signs",
        "beehives in a row", "fruit-laden branches bending", "freshly turned dark soil",
        "irrigation sprinklers catching light", "patchwork quilt on porch rail", "farm dog resting in shade",
        "preserves jars with handwritten labels", "worn leather boots by the door", "woven baskets of produce",
        "smoke from farmhouse chimney"
    ],
    lighting_conditions=[
        "early morning mist over fields", "bright midday sun with cumulus clouds",
        "golden afternoon side light", "pastoral sunset with warm sky",
        "overcast soft light flattering greens", "barn interior with dusty light shafts",
        "firefly glow at dusk", "harvest moon rising over fields"
    ],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "pan_left": 0.2, "zoom_in": 0.15, "tilt_up": 0.1},
    color_palette=["vibrant green", "earth brown", "golden wheat", "barn red"],
    mood_keywords=["peaceful", "rustic", "abundant", "pastoral", "wholesome", "nostalgic", "grounded", "honest"],
    style_prompt="lush agricultural landscape, rustic farmhouse, verdant countryside",
    time_periods=[
        "pre-dawn with roosters crowing", "early morning dew on crops",
        "golden hour with long field shadows", "midday heat shimmer over fields",
        "late afternoon harvest light", "blue hour with farmhouse lights on",
        "twilight with bats emerging", "starlit night over dark fields"
    ],
    seasons=[
        "spring planting with fresh furrows", "early summer growth explosion",
        "midsummer abundance", "harvest season with golden fields",
        "autumn after harvest with stubble fields", "early winter frost on fences",
        "deep winter with snow-covered barn", "late winter thaw with mud and promise"
    ],
    weather_conditions=[
        "morning mist burning off", "after rain with everything sparkling",
        "approaching thunderstorm over flat fields", "clear crisp autumn day",
        "light snow dusting crops", "gentle breeze rippling wheat",
        "rainbow over farmhouse", "humid summer haze",
        "frost coating every surface"
    ],
    perspectives=[
        "aerial drone over patchwork fields", "ground level through crop rows",
        "macro close-up of grain heads", "from porch looking out at fields",
        "reflection in farm pond", "inside barn looking out at daylight",
        "between vineyard rows", "from hilltop surveying the farm",
        "child's eye view through tall grass"
    ],
    narrative_themes=[
        "cycle of seasons", "honest labor", "abundance from the earth",
        "family legacy", "harmony with land", "patience rewarded",
        "self-sufficiency", "dawn to dusk rhythm", "harvest celebration",
        "roots and belonging"
    ]
)

# Domain 4: Ocean & Sea Creatures
ocean_beauty = Domain(
    name="Ocean & Sea Creatures",
    icon="🌊",
    description="Mesmerizing underwater worlds, marine life, and cinematic coastal beauty",
    locations=[
        "Coral reef ecosystem teeming with life", "Deep ocean abyssal plain",
        "Giant kelp forest canopy from below", "Rocky coastline with crashing waves",
        "Bioluminescent bay at night", "Tide pools with miniature ecosystems",
        "Ocean surface at sunset from underwater", "Underwater cave with light shaft entrance",
        "Sandy ocean floor with rays gliding", "Tidal marsh where river meets sea",
        "Whale migration route in open ocean", "Arctic Ocean under translucent sea ice",
        "Mangrove root system underwater", "Deep sea hydrothermal vent field",
        "Coral spawning event at night", "Ocean during storm from below surface",
        "Submarine canyon edge dropping into darkness", "Jellyfish lake with millions pulsing",
        "Shipwreck site colonized by marine life", "Seagrass meadow with seahorses",
        "Volcanic underwater lava meeting ocean", "Whale shark feeding at surface",
        "Antarctic krill swarm with penguins diving", "Pearl oyster bed on sandy shelf",
        "Blue hole entrance from above and below", "Manta ray cleaning station",
        "Dolphin pod in crystal clear shallows"
    ],
    signature_elements=[
        "colorful fish schools moving as one", "branching coral formations", "sea turtles gliding gracefully",
        "dolphins leaping through surface", "translucent jellyfish pulsing", "waves crashing on basalt",
        "seaweed swaying in current", "bioluminescent plankton trails", "sun rays piercing water surface",
        "bubbles rising in columns", "giant manta rays banking", "microscopic plankton clouds",
        "blue whale tail flukes", "octopus changing color and texture", "anemones with clownfish",
        "starfish on rocky substrate", "moray eel in coral crevice", "hammerhead shark silhouette",
        "sea urchin spines in detail", "cuttlefish hypnotic patterns", "humpback whale breach",
        "parrotfish biting coral", "lobster on night reef", "nudibranch vivid colors",
        "pilot fish alongside whale shark", "seahorse gripping sea fan"
    ],
    lighting_conditions=[
        "underwater sunbeams in cathedral shafts", "blue hour ocean with deep indigo",
        "golden beach sunset reflecting on waves", "bioluminescent glow of deep creatures",
        "caustic light patterns dancing on sand", "deep blue twilight zone",
        "moonlit surface seen from below", "storm light filtering through churning surface"
    ],
    camera_weights={"zoom_in": 0.25, "pan_right": 0.25, "zoom_out": 0.2, "pan_left": 0.2, "tilt_up": 0.1},
    color_palette=["deep blue", "turquoise", "coral orange", "sandy beige"],
    mood_keywords=["serene", "mysterious", "vibrant", "flowing", "majestic", "primordial", "vast", "gentle"],
    style_prompt="underwater cinematography, marine life, oceanic beauty, coastal landscapes",
    time_periods=[
        "pre-dawn ocean still as glass", "sunrise casting pink on surface",
        "golden hour with warm underwater shafts", "noon with maximum light penetration",
        "afternoon with shifting caustics", "blue hour fading to deep",
        "twilight when nocturnal creatures emerge", "midnight bioluminescence display",
        "moonrise silver on ocean surface"
    ],
    seasons=[
        "spring plankton bloom turning water green", "summer clarity with warm blue",
        "autumn migration season", "winter storm energy",
        "coral spawning season", "whale calving season",
        "sardine run season", "monsoon murky to clearing transition"
    ],
    weather_conditions=[
        "calm glassy surface", "gentle swell with rhythmic light",
        "storm waves from beneath", "after cyclone with stirred sediment clearing",
        "fog sitting on ocean surface", "rain dimpling surface seen from below",
        "trade winds creating surface chop", "dead calm with mirror reflections",
        "tidal surge in narrow channel"
    ],
    perspectives=[
        "aerial drone over reef from above", "snorkeler surface level half-in half-out",
        "macro close-up of coral polyps", "wide angle reef panorama",
        "looking up at surface from depth", "eye level with passing whale",
        "inside a school of fish", "from cave mouth looking out to blue",
        "split-shot half above half below water", "free diver descending into blue"
    ],
    narrative_themes=[
        "the hidden world beneath waves", "symbiosis and connection",
        "the deep unknown", "ocean as living entity",
        "fragile beauty", "tidal rhythms", "predator and prey dance",
        "ancient ocean unchanged", "bioluminescent magic",
        "silence of the deep"
    ]
)

# Domain 5: Lush Green Forests
lush_forests = Domain(
    name="Lush Green Forests",
    icon="🌲",
    description="Dense woodlands with towering trees, nature trails, and rich biodiversity",
    locations=[
        "Ancient forest path with cathedral canopy", "Canopy seen from mossy forest floor",
        "Sunlit forest clearing with wildflowers", "Moss-covered fallen logs and nurse trees",
        "Creek winding through old growth woods", "Fern grotto in damp hollow",
        "Sunlit glade with dust motes floating", "Dense undergrowth with filtered light",
        "Exposed root system of a giant tree", "Misty redwood grove",
        "Bamboo thicket with green-filtered light", "Forest lake with mirror reflections",
        "Hollow ancient tree trunk interior", "Mushroom colony on rotting wood",
        "Forest waterfall cascading over mossy rocks", "Abandoned forest cabin reclaimed by nature",
        "Bioluminescent fungus in dark hollow", "Canopy walkway high above forest floor",
        "Autumn forest ablaze with color", "Snow-dusted pine forest at dawn",
        "Tropical cloud forest dripping with moisture", "Birch grove with white bark and golden leaves",
        "Forest edge meeting open meadow", "Ravine with fallen tree bridge",
        "Old stone wall disappearing into woodland", "Firefly meadow at forest edge"
    ],
    signature_elements=[
        "towering ancient trees with massive trunks", "dappled sunlight through canopy gaps",
        "thick moss carpets on every surface", "unfurling fern fronds", "forest mist weaving between trunks",
        "deer pausing on a path", "fallen logs becoming nurse logs", "mushrooms in fairy rings",
        "climbing vines spiraling up trunks", "decomposing leaf litter", "spider webs catching dew drops",
        "woodpecker holes in dead snags", "lichen painting branches", "owl perched in hollow",
        "squirrel leaping between branches", "butterfly on woodland flower", "tree rings on cut stump",
        "bark beetle patterns under bark", "bracket fungus shelving on trunk",
        "canopy gap with pillar of light", "stream-polished stones", "fallen leaves floating on creek",
        "bird nest tucked in branches", "fox glimpsed through undergrowth",
        "ancient carved trail marker on tree"
    ],
    lighting_conditions=[
        "dappled forest light through leaves", "misty morning with diffused glow",
        "golden shafts breaking through canopy", "overcast soft even light",
        "blue-green filtered light in dense woods", "sunset painting treetops gold",
        "bioluminescent glow in dark hollows", "rain-filtered grey light"
    ],
    camera_weights={"tilt_up": 0.3, "zoom_in": 0.25, "pan_right": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["forest green", "moss green", "earth brown", "dappled gold"],
    mood_keywords=["tranquil", "primordial", "lush", "mystical", "verdant", "ancient", "sheltering", "alive"],
    style_prompt="dense forest cinematography, woodland atmosphere, rich green vegetation",
    time_periods=[
        "pre-dawn with birdsong beginning", "first light touching canopy",
        "golden hour with long tree shadows", "noon with canopy fully lit",
        "late afternoon with warm side light", "blue hour in the understory",
        "twilight with fireflies emerging", "night with moonlight on canopy",
        "dawn after rain with everything dripping"
    ],
    seasons=[
        "early spring with first buds and green haze", "late spring wildflower carpet",
        "full summer dense canopy", "early autumn first color changes",
        "peak autumn with forest floor golden", "late autumn bare branches revealing structure",
        "first snow on evergreen boughs", "deep winter forest stark and quiet"
    ],
    weather_conditions=[
        "morning mist lingering between trunks", "after rain with dripping canopy",
        "light rain with sound on leaves", "clear crisp with sharp shadows",
        "snow falling silently through branches", "wind moving through canopy",
        "fog so thick trees become silhouettes", "ice storm coating every twig",
        "warm humid with visible moisture"
    ],
    perspectives=[
        "aerial drone above canopy", "forest floor looking straight up",
        "macro close-up of bark texture", "eye level along a path",
        "through a hollow log frame", "reflection in forest pool",
        "from inside tree hollow looking out", "canopy level among branches",
        "low angle along mossy log", "bird's eye through gap in canopy"
    ],
    narrative_themes=[
        "the cathedral of nature", "cycles of growth and decay",
        "hidden worlds in miniature", "the forest breathes",
        "time measured in tree rings", "sanctuary and shelter",
        "ancient wisdom of old growth", "light finding its way",
        "interdependence of all life", "the path less traveled"
    ]
)

# Domain 6: Himalayan Beauty
himalayan_beauty = Domain(
    name="Beautiful Himalayas",
    icon="🏔️",
    description="Majestic mountain peaks, serene valleys, and ancient monasteries in the world's highest ranges",
    locations=[
        "Snow-capped peaks catching first light", "Cliffside monastery with prayer wheels",
        "Alpine meadow with wildflowers and yaks", "Prayer flag bridge over gorge",
        "Glacial valley with turquoise river", "Sherpa village at dawn with smoke rising",
        "High altitude glacial lake with reflections", "Rocky mountain path with prayer stones",
        "Panoramic vista from a high pass", "Rhododendron valley in full bloom",
        "Frozen waterfall on a cliff face", "Monastery library with ancient texts",
        "Yak caravan on narrow high trail", "Mountain pass shrouded in fog",
        "Tea house along a trek route", "Star trails over Himalayan peaks",
        "Avalanche path in spring with wildflowers", "Hot springs near a glacier",
        "Suspension bridge over river canyon", "Buddhist stupa at mountain crossroads",
        "Terraced barley fields on steep slopes", "Eagle's nest viewpoint above clouds",
        "Ice cave inside a glacier", "Mountain sunrise painting peaks in sequence",
        "Remote hermitage on an impossible ledge", "River confluence of two colored waters"
    ],
    signature_elements=[
        "snow-covered mountain ridges", "colorful prayer flags fluttering", "stone stupas with painted eyes",
        "yaks grazing on high pastures", "terraced fields on steep valleys", "turquoise mountain streams",
        "Buddhist monasteries clinging to cliffs", "pine forests on lower slopes", "dramatic cliff faces",
        "mani stone walls with carved mantras", "wooden bridges with prayer wheels", "rhododendron trees in bloom",
        "himalayan blue poppies", "mountain eagles soaring", "cloud inversions in valleys",
        "juniper incense smoke", "brass prayer bells", "frozen waterfalls",
        "mountain goats on ledges", "butter lamp glow from monastery windows", "apricot blossoms in Ladakh",
        "glacier crevasses with blue ice", "porter carrying loads on steep trail",
        "wind-carved snow formations on ridges", "sunrise alpenglow on summit"
    ],
    lighting_conditions=[
        "crisp mountain light with razor shadows", "golden hour on snow peaks (alpenglow)",
        "misty valley with diffused light", "clear blue sky with intense UV clarity",
        "storm light with dramatic cloud breaks", "moonlight on snow fields",
        "butter lamp glow inside monastery", "pre-dawn indigo sky with pink summit tips"
    ],
    camera_weights={"zoom_out": 0.3, "pan_right": 0.25, "tilt_up": 0.2, "zoom_in": 0.15, "pan_left": 0.1},
    color_palette=["snow white", "sky blue", "prayer flag colors", "stone grey"],
    mood_keywords=["majestic", "serene", "spiritual", "pristine", "awe-inspiring", "remote", "ancient", "humbling"],
    style_prompt="Himalayan mountain cinematography, alpine landscapes, spiritual atmosphere",
    time_periods=[
        "pre-dawn indigo before alpenglow", "sunrise touching summit first",
        "golden hour with warm rock faces", "harsh noon with bleached snow",
        "afternoon with building clouds", "blue hour with monastery lights",
        "twilight with Venus over peaks", "midnight clear sky with Milky Way",
        "dawn breaking through mountain pass"
    ],
    seasons=[
        "deep winter with heavy snowpack", "early spring thaw with waterfalls",
        "late spring rhododendron bloom", "summer monsoon with dramatic clouds",
        "post-monsoon crystal clarity", "autumn with golden larch trees",
        "early winter first snowfall", "festival season with decorated monasteries"
    ],
    weather_conditions=[
        "crystal clear with infinite visibility", "cloud inversion filling valleys",
        "approaching snow storm", "after snowfall with fresh powder",
        "light fog in mountain passes", "fierce wind with blowing snow",
        "gentle snowfall at dusk", "rainbow after mountain rain",
        "morning frost sparkling on everything"
    ],
    perspectives=[
        "aerial drone along ridge line", "ground level on mountain trail",
        "macro close-up of prayer stone carving", "through monastery window at mountains",
        "reflection in glacial lake", "looking up at cliff monastery",
        "from peak looking down at cloud sea", "inside prayer wheel corridor",
        "across valley at distant peak", "from bridge looking at river below"
    ],
    narrative_themes=[
        "the roof of the world", "spiritual journey upward",
        "impermanence of snow and ice", "human resilience at altitude",
        "ancient paths still walked", "silence above the clouds",
        "mountain as teacher", "prayer carried by wind",
        "small villages in vast landscape", "the summit within"
    ]
)

# Domain 7: Lakeside Lifestyle
lakeside_lifestyle = Domain(
    name="Lakeside Lifestyle",
    icon="🏞️",
    description="Tranquil lake houses with boats, BBQ areas, and relaxed waterfront living",
    locations=[
        "Weathered wooden dock at dawn", "Lake house porch with rocking chairs",
        "Canoe gliding on mirror-still water", "BBQ deck with string lights",
        "Lakeside fire pit circle at dusk", "Hammock strung between birch trees",
        "Fishing spot on quiet inlet", "Sunset reflected on lake surface",
        "Morning mist lifting off water", "Boathouse with kayaks stored inside",
        "Swimming platform in middle of lake", "Adirondack chairs facing water",
        "Lake house kitchen with lake view window", "Stone pathway to water's edge",
        "Treehouse overlooking the lake", "Loon nesting area in reeds",
        "Covered bridge over lake outlet stream", "Wildflower meadow meeting lake shore",
        "Ice fishing shanty on frozen lake", "Dock at night with lanterns",
        "Paddleboard on calm morning water", "Lakeside picnic on flat rock",
        "Sauna cabin with lake plunge access", "Beaver dam at lake inlet",
        "Old rowboat pulled up on pebble beach"
    ],
    signature_elements=[
        "wooden rowboats with oars", "weathered dock chairs", "BBQ grill with smoke rising",
        "orange life jackets hanging", "fishing rods leaning on rail", "perfect lake reflections",
        "water lilies and lily pads", "painted canoes", "crackling campfire",
        "porch swing with cushions", "loon calling on water", "dragonflies over water surface",
        "pine trees framing the lake", "stone skipping ripples", "morning coffee mug on dock",
        "hanging lanterns at dusk", "fish jumping in twilight", "birch bark peeling",
        "wildflowers along shoreline", "fallen leaves floating on water",
        "red canoe against green shoreline", "mist curling off warm water",
        "old rope swing over water", "binoculars and bird guide on table",
        "vintage lake house sign"
    ],
    lighting_conditions=[
        "soft morning mist diffusing sunrise", "midday sparkle on water surface",
        "golden evening with long dock shadows", "twilight blues reflected in lake",
        "string lights and lantern glow", "moonlight path across water",
        "overcast creating perfect reflections", "fire pit glow on faces at night"
    ],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "pan_left": 0.2, "zoom_in": 0.15, "tilt_up": 0.1},
    color_palette=["lake blue", "wooden brown", "sunset orange", "nature green"],
    mood_keywords=["relaxed", "peaceful", "idyllic", "recreational", "cozy", "nostalgic", "intimate", "still"],
    style_prompt="lakeside lifestyle, waterfront living, recreational lake scenes",
    time_periods=[
        "pre-dawn with lake steaming", "sunrise with loon calls",
        "golden hour painting everything warm", "lazy midday sun",
        "late afternoon swim time", "blue hour with first fireflies",
        "twilight campfire hour", "starry night reflected in lake",
        "moonrise over treeline"
    ],
    seasons=[
        "ice-out in early spring", "spring with budding trees and nesting birds",
        "peak summer with full green canopy", "late summer with warm water and long days",
        "autumn with spectacular leaf color", "late autumn with bare trees and cold water",
        "first freeze with ice on shore", "deep winter with frozen lake and snow"
    ],
    weather_conditions=[
        "glassy calm no wind", "gentle breeze creating small ripples",
        "after rain with everything fresh", "light fog hovering over water",
        "approaching thunderstorm over lake", "snow falling on unfrozen water",
        "crisp clear autumn day", "humid summer evening",
        "rainbow reflected in lake"
    ],
    perspectives=[
        "aerial drone over lake and dock", "from dock end looking at shore",
        "water level from kayak", "through screened porch at lake",
        "reflection shot upside-down landscape", "from treehouse above",
        "underwater looking up at boat hull", "from far shore across lake",
        "macro on dewdrop with lake reflected", "from hammock framing sky and trees"
    ],
    narrative_themes=[
        "simple pleasures", "disconnect to reconnect",
        "summer memories", "family gathering place",
        "morning solitude", "nature's soundtrack",
        "time slows here", "seasons of the lake",
        "childhood summers", "the lake remembers"
    ]
)

# Domain 8: Colorful American Roads
colorful_roads = Domain(
    name="Colorful American Roads",
    icon="🛣️",
    description="Scenic highways covered with autumn foliage and vibrant tree canopies",
    locations=[
        "Winding mountain road through forest", "Tree tunnel with arching branches",
        "Scenic overlook with valley view", "Country road through autumn forest",
        "Blue Ridge Parkway in fall color", "Covered bridge on back road",
        "Road beside a rushing mountain stream", "Vista point at mountain summit",
        "Foliage-lined highway with center stripe", "Desert highway through red rock country",
        "Pacific Coast Highway cliff section", "New England village road with white church",
        "Appalachian ridgetop road above clouds", "Farm road lined with stone walls and maples",
        "Road through aspen grove in Colorado", "Bayou road with Spanish moss canopy",
        "Road switchback revealing valley below", "Historic Route 66 section with neon",
        "Mountain pass road with snowcapped peaks", "Road through Joshua Tree landscape",
        "Coastal road with crashing waves below", "Road through rolling Kansas wheat fields",
        "Autumn road with leaves blowing across", "Bridge road over wide river valley",
        "Forest service road with wildflower shoulders", "Two-lane road vanishing to horizon"
    ],
    signature_elements=[
        "colorful autumn leaves in full spectrum", "winding asphalt disappearing around curve",
        "tree canopies forming tunnel overhead", "mountain vistas in layered blue",
        "fallen leaves carpeting road shoulders", "white and yellow road lines",
        "rustic guard rails along drops", "road signs weathered by seasons",
        "distant mountains framing the road", "stone walls along country roads",
        "pickup truck on empty road", "morning mist on road surface",
        "deer crossing sign", "covered bridge entrance framing fall color",
        "mile marker posts", "roadside wildflower patches", "reflective road markers at dusk",
        "double yellow line on curve", "steam rising from wet asphalt after rain",
        "old gas station at crossroads", "mailboxes along rural road",
        "split rail fence beside road", "road cutting through rock face",
        "bridge over creek with autumn reflections", "motorcyclist on sweeping curve"
    ],
    lighting_conditions=[
        "golden autumn light filtering through leaves", "soft overcast enhancing fall colors",
        "sun through trees creating shadow stripes", "vibrant midday saturating colors",
        "early morning with long road shadows", "sunset behind mountain road",
        "fog diffusing headlights", "rain-wet road reflecting autumn color"
    ],
    camera_weights={"pan_right": 0.35, "zoom_in": 0.25, "pan_left": 0.2, "zoom_out": 0.15, "tilt_up": 0.05},
    color_palette=["autumn red", "golden yellow", "orange", "forest green"],
    mood_keywords=["scenic", "colorful", "peaceful", "journey", "autumnal", "nostalgic", "wanderlust", "free"],
    style_prompt="autumn road cinematography, colorful foliage, scenic highway",
    time_periods=[
        "pre-dawn empty road with rising mist", "sunrise painting treetops",
        "golden hour with warm road glow", "midday with peak color saturation",
        "late afternoon with long shadows", "blue hour with headlights beginning",
        "twilight with last color in sky", "night with moonlit road"
    ],
    seasons=[
        "early autumn first color changes", "peak fall foliage",
        "late autumn mostly bare with some holdouts", "early winter bare trees and first snow",
        "spring green tunnel forming", "summer full green canopy",
        "Indian summer late warmth", "spring with roadside wildflowers"
    ],
    weather_conditions=[
        "light fog in valleys", "crisp clear autumn day",
        "after rain with glistening leaves", "light drizzle with moody sky",
        "wind blowing leaves across road", "first snowflakes mixing with fall color",
        "approaching storm with dramatic sky", "golden light breaking through clouds"
    ],
    perspectives=[
        "aerial drone following road from above", "driver's POV through windshield",
        "macro close-up of wet leaves on asphalt", "standing in center of empty road",
        "from hillside looking down at switchback", "through car mirror at road behind",
        "low angle along road surface", "from covered bridge looking out",
        "panoramic from overlook", "between stone wall and road edge"
    ],
    narrative_themes=[
        "the open road calls", "journey over destination",
        "nature's last hurrah", "roads less traveled",
        "solitary drive", "changing seasons changing landscapes",
        "America's backroads", "wandering without purpose",
        "the curve ahead", "freedom of the road"
    ]
)

# Domain 9: Antarctica Beauty
antarctica = Domain(
    name="Antarctica Beauty",
    icon="🐧",
    description="Pristine polar landscapes with ice formations, wildlife, and extreme beauty",
    locations=[
        "Ice shelf edge calving into sea", "Emperor penguin colony on sea ice",
        "Glacial ice cave with blue walls", "Iceberg field with sculpted arches",
        "Research station in blizzard", "Seal haul-out on rocky beach",
        "Frozen ocean surface stretching to horizon", "Towering ice cliffs reflecting in water",
        "Polar plateau with wind-carved sastrugi", "Volcanic hot springs on Deception Island",
        "Penguin highway trail worn into snow", "Tabular iceberg the size of a city",
        "Zodiac boat among ice cathedral", "Abandoned whaling station ruins",
        "Snow petrel nesting colony on nunatak", "Leopard seal hunting near ice edge",
        "Dry valleys with exposed rock", "Crevasse field on glacier surface",
        "Brash ice floating in bay", "Whale blow visible from ice cliff",
        "Pressure ridges where ice plates collide", "Underwater view beneath sea ice",
        "Wind-polished blue ice runway", "Glacier tongue meeting the ocean",
        "Moss patch one of few Antarctic plants", "Southern lights over ice sheet"
    ],
    signature_elements=[
        "massive tabular icebergs", "penguin colonies in thousands", "translucent blue glacial ice",
        "aurora australis dancing overhead", "Weddell seals on ice", "ice formations sculpted by wind",
        "snow-covered mountain peaks", "frozen ocean stretching endlessly", "research vessel in ice field",
        "penguin chicks huddling", "crevasse revealing deep blue", "wind-carved snow sastrugi",
        "ice shelf edge hundreds of feet tall", "whale breaching near ice", "skua birds in flight",
        "icicles hanging from overhangs", "snow crystals in macro", "volcanic steam against ice",
        "krill swarms beneath ice", "ice pancakes forming on surface",
        "frost flowers on new sea ice", "sun dogs (parhelia) in polar sky",
        "leopard seal yawning showing teeth", "ice cave ceiling with light coming through",
        "penguin footprints in fresh snow"
    ],
    lighting_conditions=[
        "polar daylight with low angle sun", "blue hour that lasts for hours",
        "aurora australis green and purple", "pristine white light reflected off snow",
        "golden sun at midnight (polar summer)", "deep twilight of approaching polar night",
        "storm light with snow blowing horizontally", "sun behind iceberg creating halo"
    ],
    camera_weights={"zoom_out": 0.3, "pan_right": 0.25, "zoom_in": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["ice blue", "pristine white", "aurora green", "deep ocean blue"],
    mood_keywords=["pristine", "extreme", "majestic", "remote", "otherworldly", "vast", "silent", "raw"],
    style_prompt="Antarctic landscape, polar cinematography, glacial ice beauty",
    time_periods=[
        "polar dawn after months of darkness", "midnight sun golden on ice",
        "noon with sun circling near horizon", "blue hour extending for hours",
        "brief sunset in shoulder season", "aurora time in polar night",
        "whiteout conditions at midday", "crystal clear midnight",
        "sunrise and sunset happening simultaneously"
    ],
    seasons=[
        "deep polar winter with total darkness", "spring return of sunlight",
        "summer with 24-hour daylight", "autumn with sea ice forming",
        "breeding season for penguins", "whale feeding season",
        "sea ice breakup in late spring", "blizzard season"
    ],
    weather_conditions=[
        "crystal clear with infinite visibility", "blizzard with zero visibility",
        "light snow falling gently", "fierce katabatic winds",
        "calm windless rare day", "fog rolling over ice shelf",
        "ice crystals suspended in air (diamond dust)", "approaching storm wall",
        "clear after storm with fresh snow"
    ],
    perspectives=[
        "aerial drone over penguin colony", "ice level floating among bergs",
        "macro close-up of ice crystals", "from zodiac boat in ice field",
        "looking up at ice cliff face", "underwater beneath sea ice",
        "from research station window", "panoramic from mountain top",
        "between pressure ridges", "penguin's eye level on belly"
    ],
    narrative_themes=[
        "last untouched wilderness", "survival against extremes",
        "ice as living sculpture", "community in isolation",
        "the weight of silence", "climate's front line",
        "beauty in harshness", "cycles of ice and light",
        "life finds a way", "the white continent speaks"
    ]
)

# Domain 10: Life in Space
space_life = Domain(
    name="Life in Space",
    icon="🚀",
    description="Cosmic beauty with planets, nebulae, space stations, and celestial wonders",
    locations=[
        "International Space Station cupola view", "Nebula field with star formation",
        "Mars surface with Olympus Mons", "Asteroid belt with tumbling rocks",
        "Deep space vista with galaxy arm", "Space station interior with floating objects",
        "Lunar surface with Earth rising", "Saturn's rings from edge-on",
        "Starfield with Milky Way core", "Comet tail streaming past observer",
        "Jupiter's Great Red Spot close approach", "Space walk with Earth below",
        "Binary star system with orbital dance", "Ice moon Europa surface with cracks",
        "Meteor shower seen from orbit", "Supernova remnant expanding cloud",
        "Planetary ring system from within", "Black hole accretion disk",
        "Space station docking sequence", "Titan's methane lakes",
        "Lunar crater floor with long shadows", "Solar prominences erupting",
        "Kuiper Belt objects in dim sunlight", "Galaxy collision in progress",
        "Pulsar beaming across dark space", "Exoplanet atmosphere at terminator line"
    ],
    signature_elements=[
        "brilliant stars against void", "colorful gas nebulae", "ringed planet majesty",
        "space station solar panels", "communication satellites", "cosmic dust lanes",
        "spiral galaxies viewed from angle", "tumbling asteroids", "Earth as blue marble",
        "zero gravity floating objects", "rocket engine exhaust plumes", "solar flares erupting",
        "comet nucleus outgassing", "planetary auroras", "space suit visor reflections",
        "star clusters glittering", "dark matter gravitational lensing effect",
        "ion drive blue glow", "docking mechanisms", "micro-meteorite impacts",
        "tidal forces distorting moons", "light bending near massive object",
        "crystalline ice particles", "radio telescope dish pointed at stars",
        "constellation patterns connecting stars"
    ],
    lighting_conditions=[
        "single harsh sunlight in vacuum", "nebula glow in multiple colors",
        "Earth shine illuminating spacecraft", "starlight on dark surfaces",
        "solar flare intensity", "bioluminescent-like nebula emission",
        "reflected planet light on moon surface", "total darkness broken by distant sun"
    ],
    camera_weights={"zoom_in": 0.3, "zoom_out": 0.3, "pan_right": 0.2, "pan_left": 0.15, "tilt_up": 0.05},
    color_palette=["deep space black", "nebula purple", "star white", "planet blue"],
    mood_keywords=["infinite", "cosmic", "awe-inspiring", "mysterious", "vast", "silent", "lonely", "transcendent"],
    style_prompt="space cinematography, cosmic scenes, celestial beauty, astronomical wonders",
    time_periods=[
        "orbital sunrise painting station gold", "deep space eternal night",
        "eclipse shadow crossing a moon", "solar maximum activity period",
        "star formation region in process", "galactic twilight at edge of arm",
        "pulsar flash rhythm", "comet perihelion approach",
        "planetary conjunction alignment"
    ],
    seasons=[
        "solar maximum with active sun", "solar minimum with quiet sun",
        "meteor shower peak", "eclipse season",
        "opposition of outer planet", "comet apparition",
        "aurora season on Jupiter", "ring plane crossing of Saturn"
    ],
    weather_conditions=[
        "solar wind stream hitting magnetosphere", "cosmic ray shower",
        "dust storm on Mars surface", "ammonia clouds on Jupiter",
        "methane rain on Titan", "diamond rain on Neptune",
        "calm interplanetary space", "solar prominence eruption",
        "micro-meteorite field"
    ],
    perspectives=[
        "cupola window looking down at Earth", "spacewalk POV looking at stars",
        "telescope deep field zoom", "from planet surface looking up",
        "orbiting around a celestial body", "approaching through asteroid field",
        "from inside ring system", "macro on space suit detail",
        "wide angle galaxy panorama", "from behind moon at Earth"
    ],
    narrative_themes=[
        "human smallness cosmic vastness", "frontier of exploration",
        "beauty in the void", "home planet from afar",
        "cosmic timescales", "worlds beyond imagination",
        "silence speaks loudest", "gravity's embrace",
        "the overview effect", "we are stardust"
    ]
)

# Domain 11: Luxury Cruise Ships
luxury_cruise = Domain(
    name="Luxury Cruise Ships",
    icon="🚢",
    description="Opulent cruise ship life with pools, dining, entertainment, and ocean views",
    locations=[
        "Pool deck with ocean panorama", "Grand dining hall with crystal chandelier",
        "Penthouse suite with balcony", "Broadway-style theater",
        "Sky lounge with 360 views", "Thermal spa and vitality pool",
        "Casino floor with ambient lighting", "Observation deck at bow",
        "Captain's bridge with instrument panels", "Teak promenade deck",
        "Library bar with leather chairs", "Art gallery corridor",
        "Rock climbing wall with ocean backdrop", "Sushi bar with live preparation",
        "Helicopter pad with sunset view", "Ice bar with frozen sculptures",
        "Wine tasting cellar at sea", "Infinity pool merging with horizon",
        "Private dining pod on upper deck", "Garden terrace with real trees",
        "Jazz club with intimate stage", "Water slide complex",
        "Cigar lounge with port views", "Tender launch platform",
        "Morning yoga deck at sunrise", "Private island beach club stop"
    ],
    signature_elements=[
        "infinity pools blending with ocean", "elegant multi-course dining setup",
        "crystal chandeliers in grand spaces", "panoramic ocean views everywhere",
        "teak deck chairs in rows", "champagne service on deck",
        "entertainment stages with lighting", "luxury cabin with ocean balcony",
        "floor-to-ceiling panoramic windows", "sunset cocktails at railing",
        "white-gloved service", "fresh flower arrangements", "art deco details",
        "spiral staircase with glass rail", "ship wake trailing to horizon",
        "midnight buffet display", "port of call approaching", "dolphins in bow wave",
        "cruise director's microphone", "moonlight on open ocean",
        "lifeboat row with orange covers", "ship horn sounding",
        "anchor chain descending", "pilot whale alongside ship",
        "flag ceremony at stern"
    ],
    lighting_conditions=[
        "golden ocean sunset from deck", "elegant interior chandelier warmth",
        "poolside glow with underwater lights", "starlit deck with ambient fixtures",
        "sunrise through suite windows", "theater spotlight drama",
        "casino neon and ambient mix", "moonlight on teak deck"
    ],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "zoom_in": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["ocean blue", "luxury gold", "pristine white", "sunset orange"],
    mood_keywords=["luxurious", "relaxing", "opulent", "elegant", "adventurous", "indulgent", "refined", "cosmopolitan"],
    style_prompt="luxury cruise ship, elegant maritime lifestyle, upscale travel",
    time_periods=[
        "dawn departure from port", "morning at sea with calm waters",
        "golden hour cocktails on deck", "midnight under stars at sea",
        "noon pool party energy", "blue hour dinner service",
        "twilight approaching new port", "sunrise yoga on top deck"
    ],
    seasons=[
        "Caribbean winter cruise", "Mediterranean summer voyage",
        "Alaska glacier season", "autumn New England cruise",
        "Antarctic expedition season", "spring transatlantic crossing",
        "holiday season festive cruise", "monsoon repositioning voyage"
    ],
    weather_conditions=[
        "perfectly calm sea", "gentle rolling swell",
        "light rain on deck surfaces", "brilliant tropical sunshine",
        "fog with ship horn sounding", "northern lights on arctic route",
        "dramatic clouds at sunset", "balmy warm evening breeze"
    ],
    perspectives=[
        "aerial drone circling ship", "from tender approaching ship",
        "through porthole frame", "from pool looking up at decks",
        "bow perspective watching waves part", "from crow's nest above",
        "reflection in polished brass", "wide angle atrium looking up",
        "from dock watching ship depart", "underwater at anchor"
    ],
    narrative_themes=[
        "floating palace", "escape from routine",
        "the journey is the destination", "luxury at sea",
        "sunsets collected", "cultures connected by water",
        "grand tradition of ocean travel", "community of strangers",
        "the horizon beckons", "time suspended at sea"
    ]
)

# Domain 12: Luxury Yachts
luxury_yachts = Domain(
    name="Luxury Yachts",
    icon="⛵",
    description="Private yacht lifestyle with exclusivity, ocean adventures, and premium amenities",
    locations=[
        "Sleek yacht deck with teak flooring", "Helm station with advanced navigation",
        "Master cabin with panoramic hull windows", "Flybridge lounge with wet bar",
        "Sundeck with sunpads and shade", "Water sports platform lowered to sea",
        "Formal dining area with ocean view", "Jacuzzi on upper deck",
        "Superyacht marina berth in Monaco", "Open ocean cruising at speed",
        "Anchored in secluded turquoise cove", "Beach club at stern water level",
        "Engine room cathedral of engineering", "Crew galley preparing gourmet",
        "Tender garage with jet skis", "Wine cellar in hull",
        "Master bathroom with sea view", "Bow lounge with trampoline net",
        "Helipad on upper deck", "Night passage under stars",
        "Anchored near volcanic island", "Sailing yacht under full canvas",
        "Catamaran deck between hulls", "Ice-class yacht near glacier",
        "Yacht in regatta under spinnaker"
    ],
    signature_elements=[
        "sleek hull cutting through water", "teak deck with perfect grain",
        "leather seating with contrast stitching", "jet skis and water toys deployed",
        "champagne in crystal stemware", "ocean spray on polished steel",
        "sunset from flybridge", "hand-stitched leather helm wheel",
        "navigation screens glowing blue", "anchor chain descending into turquoise",
        "wake pattern from above", "polished stainless railings",
        "custom lighting under gunwale", "tender launch and recovery",
        "flag and ensign flying", "underwater lights at night",
        "chef plating on deck galley", "swimming platform at water level",
        "mooring lines on cleats", "wind in yacht burgee",
        "sonar display of seafloor", "binoculars on helm console",
        "folded towels and fresh flowers", "yacht name on stern in gold",
        "drone shot of yacht from above"
    ],
    lighting_conditions=[
        "bright ocean sun with sparkle", "golden hour at sea",
        "yacht interior ambient mood lighting", "moonlit water from deck",
        "underwater hull lights creating glow", "sunrise on anchor watch",
        "storm approaching with dramatic sky", "night passage with instruments glowing"
    ],
    camera_weights={"pan_right": 0.3, "zoom_in": 0.25, "zoom_out": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["yacht white", "ocean blue", "teak brown", "chrome silver"],
    mood_keywords=["exclusive", "luxurious", "adventurous", "prestigious", "free", "intimate", "refined", "powerful"],
    style_prompt="luxury yacht lifestyle, private maritime, upscale boating",
    time_periods=[
        "dawn anchor watch", "morning swim off stern",
        "golden hour cocktails on flybridge", "noon under blazing sun",
        "afternoon water sports", "blue hour departure",
        "twilight dinner on deck", "midnight passage under stars",
        "sunrise arrival at new island"
    ],
    seasons=[
        "Mediterranean high summer", "Caribbean winter charter",
        "South Pacific spring sailing", "autumn Adriatic cruise",
        "monsoon Indian Ocean passage", "summer solstice Nordic fjord",
        "regatta week", "off-season refit and launch"
    ],
    weather_conditions=[
        "flat calm mirror water", "perfect sailing breeze",
        "building swell on passage", "tropical squall passing",
        "crystal clear visibility to seafloor", "light chop with spray",
        "fog requiring radar navigation", "post-storm rainbow over anchorage"
    ],
    perspectives=[
        "aerial drone tracking shot", "from water level looking up at hull",
        "helm POV over bow", "underwater looking up at hull",
        "from tender approaching yacht", "through porthole from inside",
        "from masthead looking down", "wide shot anchored in cove",
        "macro on polished detail", "from beach watching yacht arrive"
    ],
    narrative_themes=[
        "freedom of the seas", "ultimate privacy",
        "the art of seamanship", "design meets ocean",
        "adventures in paradise", "life at anchor",
        "the yacht as home", "exploring coastlines",
        "wind and water mastery", "privilege meets responsibility"
    ]
)

# Domain 13: Desert Life Worldwide
desert_life = Domain(
    name="Desert Life Worldwide",
    icon="🏜️",
    description="Vast desert landscapes from Sahara to Arabian to American deserts with unique beauty",
    locations=[
        "Towering sand dunes with sharp crests", "Desert oasis with date palms",
        "Slot canyon with striped walls", "Blinding white salt flats",
        "Balanced rock formations", "Desert sunset with silhouetted saguaros",
        "Bedouin camp with woven tents", "Cactus field in Sonoran desert",
        "Desert night sky with Milky Way", "Ancient caravan route with worn stones",
        "Wind-sculpted sandstone arches", "Desert canyon with flash flood marks",
        "Sand sea stretching to horizon", "Desert spring wildflower super-bloom",
        "Petrified forest with stone trees", "Desert mesa with flat top and sheer sides",
        "Mirage shimmering on flat desert", "Volcanic desert with black lava fields",
        "White Sands gypsum dune field", "Desert monastery built into cliff",
        "Wadi with rare water flowing", "Desert railway track straight to vanishing point",
        "Joshua Tree landscape at twilight", "Sand storm approaching wall of dust",
        "Desert hot spring with mineral deposits", "Fairy chimney formations in cappadocia"
    ],
    signature_elements=[
        "rippled sand patterns from wind", "saguaro cacti silhouettes", "camel caravan in line",
        "dramatic rock formations and hoodoos", "heat shimmer distorting horizon", "desert wildflowers after rain",
        "sand storms rolling across dunes", "oasis palm reflections in water", "star-filled sky with no light pollution",
        "dramatic shadow patterns at low sun", "cracked dry earth patterns", "desert fox or fennec",
        "hawk circling on thermals", "tumbleweeds rolling", "sand cascading down dune face",
        "tortoise crossing sand", "lizard on sun-baked rock", "ancient petroglyphs on canyon wall",
        "desert beetle tracks in sand", "wind erosion revealing geological layers",
        "salt crystal formations", "ocotillo in bloom", "dust devil spinning",
        "nomad silhouette against sky", "geometric patterns in dried mud"
    ],
    lighting_conditions=[
        "harsh midday sun with deep shadows", "golden hour painting dunes",
        "blue hour with purple desert", "starlit night revealing Milky Way",
        "sunrise catching dune crests first", "sandstorm diffusing light to orange",
        "slot canyon reflected light bouncing", "full moon on white sand"
    ],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "tilt_up": 0.2, "zoom_in": 0.15, "pan_left": 0.1},
    color_palette=["golden sand", "desert orange", "sky blue", "earth red"],
    mood_keywords=["vast", "harsh", "serene", "timeless", "dramatic", "stark", "ancient", "contemplative"],
    style_prompt="desert cinematography, arid landscapes, sand dunes, desert life",
    time_periods=[
        "pre-dawn cold desert with frost", "sunrise lighting dune crests",
        "golden hour with long dune shadows", "harsh noon with no shadows",
        "afternoon heat shimmer", "blue hour with cooling air",
        "twilight silhouettes", "midnight star photography time",
        "3am with Milky Way overhead"
    ],
    seasons=[
        "spring wildflower super-bloom", "scorching summer heat",
        "autumn cooling with clear skies", "winter with cold nights and warm days",
        "monsoon season with rare rain", "dry season at peak aridity",
        "sandstorm season", "cool season perfect for travel"
    ],
    weather_conditions=[
        "perfectly clear endless blue sky", "approaching sandstorm wall",
        "after rare rain with wet sand", "dust devil season",
        "heat haze distorting horizon", "cold front bringing frost",
        "light wind creating sand streamers", "flash flood warning clouds",
        "dew on desert plants at dawn"
    ],
    perspectives=[
        "aerial drone over dune sea", "ground level along sand ripples",
        "macro close-up of sand grains", "from inside slot canyon looking up",
        "on dune crest looking both ways", "from oasis looking at desert",
        "through heat shimmer", "from canyon rim looking down",
        "inside tent looking out at desert", "at water hole level"
    ],
    narrative_themes=[
        "emptiness as fullness", "survival and adaptation",
        "ancient trade routes", "silence of vast spaces",
        "water as life", "night sky revelation",
        "wind as sculptor", "desert bloom miracle",
        "nomadic freedom", "geological deep time"
    ]
)

# Domain 14: Tropical Greenery
tropical_greenery = Domain(
    name="Tropical Greenery (Indonesia, Kerala)",
    icon="🌴",
    description="Lush tropical vegetation with rice terraces, palm trees, and soothing green landscapes",
    locations=[
        "Terraced rice paddy fields cascading down hillside", "Tropical waterfall into emerald pool",
        "Coconut palm grove with filtered light", "Jungle canopy from above",
        "Bamboo forest with creaking sounds", "Tropical beach with palm overhang",
        "Village nestled in green mountains", "River winding through dense jungle",
        "Tea plantation rows on misty hills", "Lotus pond at a Hindu temple",
        "Spice garden with cinnamon and cardamom", "Backwater houseboat scene in Kerala",
        "Volcanic lake surrounded by jungle", "Mangrove forest with root labyrinths",
        "Tropical botanical garden", "Rubber plantation with neat tree rows",
        "Rice harvest with golden paddies", "Jungle rope bridge over gorge",
        "Hot spring in tropical forest", "Clove plantation fragrant at dawn",
        "Tropical river cave with bats", "Butterfly garden with hundreds of species",
        "Durian orchard at fruiting time", "Fish pond in rice paddy system",
        "Mountain waterfall chain series", "Tropical village market with produce"
    ],
    signature_elements=[
        "sculpted rice terrace levels", "coconut palms swaying", "tropical orchids and hibiscus",
        "broad banana leaves with water drops", "cascading waterfalls", "dense layered vegetation",
        "traditional thatched huts", "exotic tropical birds", "thick jungle vines",
        "lotus flowers on still water", "tea pickers on misty slopes", "temple offerings of flowers",
        "buffalo in flooded paddy", "gecko on palm trunk", "tropical fruit displays",
        "fireflies in evening jungle", "spider webs catching morning dew", "frangipani tree in bloom",
        "carved stone deity in garden", "dragonflies over paddy water",
        "monkeys in treetops", "elephant bathing in river", "turmeric flowers in spice garden",
        "rainbow through waterfall mist", "traditional fishing nets in backwater"
    ],
    lighting_conditions=[
        "soft tropical light filtered by clouds", "monsoon dramatic cloud formations",
        "dappled jungle sun through canopy", "misty morning on tea hills",
        "golden hour on rice terraces", "overcast soft flattering green tones",
        "rain-filtered grey with lush saturation", "sunrise through palm silhouettes"
    ],
    camera_weights={"pan_right": 0.3, "zoom_in": 0.25, "zoom_out": 0.2, "tilt_up": 0.15, "pan_left": 0.1},
    color_palette=["vibrant green", "tropical blue", "earth brown", "flower colors"],
    mood_keywords=["lush", "tranquil", "tropical", "verdant", "peaceful", "exotic", "abundant", "humid"],
    style_prompt="tropical landscape, lush greenery, rice terraces, tropical paradise",
    time_periods=[
        "pre-dawn with mist in valleys", "sunrise through palm trees",
        "golden hour on terraces", "midday tropical intensity",
        "afternoon rain shower", "blue hour with fireflies",
        "twilight temple ceremony time", "night with jungle sounds",
        "dawn with farmers heading to fields"
    ],
    seasons=[
        "monsoon peak with dramatic rain", "post-monsoon lush green maximum",
        "dry season with clear skies", "rice planting season",
        "harvest season with golden paddies", "flowering season",
        "fruit season with heavy branches", "cool season in highlands"
    ],
    weather_conditions=[
        "morning mist in valleys", "tropical downpour",
        "clearing after rain with rainbow", "humid haze",
        "crisp cool highland morning", "monsoon clouds building",
        "gentle warm rain", "perfectly clear tropical day",
        "steam rising from warm earth after rain"
    ],
    perspectives=[
        "aerial drone over rice terraces", "ground level through paddy water",
        "macro close-up of tropical flower", "from houseboat on backwater",
        "looking up through palm canopy", "from temple steps at landscape",
        "inside bamboo forest looking along path", "from waterfall pool looking up",
        "bird's eye of village in green", "through banana leaf frame"
    ],
    narrative_themes=[
        "abundance of the tropics", "water as life giver",
        "ancient agricultural wisdom", "layers of green",
        "coexistence with nature", "monsoon rhythms",
        "spice and fragrance", "the green cathedral",
        "village simplicity", "fertility of volcanic soil"
    ]
)

# Domain 15: Buddhist Lifestyle
buddhist_lifestyle = Domain(
    name="Buddhist Lifestyle & Temples",
    icon="🕉️",
    description="Tibetan monasteries, temples, prayer flags, and spiritual landscapes across Buddhist regions",
    locations=[
        "Mountain monastery perched on cliff", "Prayer wheel hall with spinning drums",
        "Temple interior with golden Buddha", "Meditation cave with single cushion",
        "Stupa courtyard with circumambulation path", "Monk quarters with simple furnishings",
        "Prayer flag ridge against blue sky", "Buddhist shrine with flower offerings",
        "Zen temple garden with raked gravel", "Monastery kitchen preparing communal meal",
        "Ancient Bodhi tree with prayer scarves", "Alms-giving procession at dawn",
        "Tibetan scripture printing room", "Pagoda rising through morning mist",
        "Sand mandala creation in progress", "Meditation hall with rows of cushions",
        "Monastery rooftop with mountain views", "Forest monastery in Thailand",
        "Cave temple with painted ceiling", "Reclining Buddha in ancient ruins",
        "Bell tower with enormous bronze bell", "Lotus pond before temple entrance",
        "Monk's path through bamboo grove", "Debating courtyard with monks",
        "Butter sculpture workshop", "Reliquary chamber with offerings"
    ],
    signature_elements=[
        "prayer flags in five colors fluttering", "golden Buddha statues in various poses",
        "prayer wheels spinning with mantras", "monks in saffron or maroon robes",
        "incense smoke curling upward", "intricate mandala artwork",
        "singing bowl resonating", "butter lamps flickering rows",
        "thangka paintings on silk", "stone mani walls stretching along paths",
        "temple bells ringing in wind", "dharma wheel symbol",
        "meditation beads (mala)", "offering bowls with water",
        "roof-edge decorative dharma symbols", "lotus flower motifs everywhere",
        "prostrating pilgrim", "sacred texts wrapped in cloth",
        "conch shell ceremonial horn", "temple guardian statues",
        "rain chains at temple eaves", "monastery cat sleeping in sun",
        "prayer scarves tied to sacred tree", "monk's sandals at temple door",
        "dawn drum calling to practice"
    ],
    lighting_conditions=[
        "soft temple light through paper screens", "golden hour on mountain monastery",
        "candlelit and butter lamp interior warmth", "misty morning around pagoda",
        "incense-filtered hazy light", "moonlight on white stupa",
        "sunrise hitting golden spire first", "overcast contemplative light"
    ],
    camera_weights={"tilt_up": 0.3, "zoom_in": 0.25, "pan_right": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["saffron orange", "prayer flag colors", "gold", "temple red"],
    mood_keywords=["spiritual", "peaceful", "sacred", "meditative", "timeless", "contemplative", "reverent", "serene"],
    style_prompt="Buddhist temple cinematography, spiritual atmosphere, Tibetan culture",
    time_periods=[
        "pre-dawn meditation bell", "sunrise on golden spire",
        "golden hour on monastery walls", "noon with sharp temple shadows",
        "afternoon teaching time", "blue hour with butter lamps lit",
        "twilight chanting hour", "midnight meditation vigil",
        "dawn alms round"
    ],
    seasons=[
        "Tibetan New Year (Losar)", "monsoon retreat (Vassa)",
        "autumn teaching season", "winter meditation intensive",
        "spring thaw and renewal", "Vesak full moon celebration",
        "summer pilgrim season", "harvest offering festival"
    ],
    weather_conditions=[
        "morning mist around monastery", "clear mountain air",
        "light rain on temple roof", "snow on monastery courtyard",
        "fog making stupas appear and disappear", "wind carrying prayer flag mantras",
        "gentle sun warming stone walls", "post-rain rainbow over temple",
        "incense smoke mixing with fog"
    ],
    perspectives=[
        "aerial revealing monastery layout", "ground level prostration view",
        "macro close-up of prayer wheel detail", "through temple doorway at Buddha",
        "from courtyard looking up at spire", "reflection in offering water bowl",
        "along monastery corridor", "from meditation cushion POV",
        "through incense smoke", "from rooftop at surrounding landscape"
    ],
    narrative_themes=[
        "the path to awakening", "simplicity as freedom",
        "devotion expressed in art", "silence and stillness",
        "impermanence in stone and paint", "community of practice",
        "mountain and monastery as one", "the sound of one bell",
        "pilgrimage as transformation", "inner landscape mirrors outer"
    ]
)

# Domain 16: Ancient European Cities
ancient_european = Domain(
    name="Ancient European Cities",
    icon="🏰",
    description="Historic European cities with cobblestone streets, medieval architecture, and timeless beauty",
    locations=[
        "Cobblestone plaza with central fountain", "Medieval castle on hilltop",
        "Gothic cathedral interior with rose window", "Narrow alleyway with hanging laundry",
        "Grand town square with cafe terraces", "Ancient stone bridge over river",
        "City walls with watchtower walkway", "Medieval market street with timber frames",
        "Gothic architecture with flying buttresses", "Renaissance palazzo courtyard",
        "Canal-side buildings with reflections", "Monastery cloister with herb garden",
        "Roman forum ruins within modern city", "Bell tower overlooking terracotta roofs",
        "Underground medieval cellar tavern", "Castle drawbridge and moat",
        "Baroque opera house interior", "Winding staircase in tower",
        "Harbor with fishing boats and old buildings", "Vineyard on city outskirts with skyline",
        "Medieval guild hall with timber ceiling", "Gas-lit passage between buildings",
        "Rooftop terrace overlooking old town", "Ancient aqueduct entering city",
        "Flower market in historic square", "Library in former church"
    ],
    signature_elements=[
        "cobblestone streets worn smooth", "Gothic spires reaching skyward",
        "wrought iron gas lamps", "ivy-covered stone walls",
        "cafe terraces with wicker chairs", "church bells ringing",
        "medieval towers with crenellations", "stone bridges with arches",
        "baroque facade ornamentation", "terracotta roof tiles in warm tones",
        "timber-framed upper stories", "carved stone doorways",
        "window boxes with geraniums", "narrow passages opening to squares",
        "fountain sculpture detail", "cathedral rose window light",
        "chimney pots on skyline", "brass door knockers",
        "worn stone steps with groove from centuries", "hanging shop signs in wrought iron",
        "church organ pipes", "mosaic floor in basilica",
        "gargoyles and water spouts", "sundial on ancient wall",
        "market stalls under medieval arches"
    ],
    lighting_conditions=[
        "golden afternoon on limestone facades", "foggy morning gas lamp glow",
        "twilight blue with warm window light", "warm street lamps on wet cobblestones",
        "cathedral interior with stained glass color", "sunrise on rooftop panorama",
        "overcast diffused light on grey stone", "candlelit interior of old tavern"
    ],
    camera_weights={"pan_right": 0.3, "zoom_in": 0.25, "tilt_up": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["aged stone", "terracotta", "slate grey", "warm cream"],
    mood_keywords=["historic", "romantic", "timeless", "charming", "atmospheric", "elegant", "storied", "intimate"],
    style_prompt="European historic city, medieval architecture, cobblestone streets",
    time_periods=[
        "pre-dawn empty streets with lamp glow", "sunrise on bell tower",
        "golden hour on plaza facades", "midday with sharp building shadows",
        "late afternoon cafe culture", "blue hour with lights coming on",
        "twilight with church silhouette", "midnight with moonlit rooftops",
        "dawn with baker's light in window"
    ],
    seasons=[
        "spring with window boxes blooming", "summer with outdoor dining everywhere",
        "autumn with leaves on cobblestones", "winter with Christmas markets",
        "early spring rain on stone streets", "late summer festival season",
        "harvest time with wine and food fairs", "deep winter with empty atmospheric streets"
    ],
    weather_conditions=[
        "light fog wrapping around towers", "after rain with glistening cobblestones",
        "light snow on medieval rooftops", "clear crisp winter day",
        "gentle spring rain with umbrellas", "warm summer evening breeze",
        "dramatic storm clouds over castle", "frost on morning cobblestones"
    ],
    perspectives=[
        "aerial drone over old town rooftops", "ground level along cobblestone street",
        "macro close-up of carved stone detail", "through arched gateway into square",
        "reflection in canal or puddle", "looking up at cathedral ceiling",
        "from bridge at waterfront buildings", "from tower balcony at city below",
        "through window at street scene", "narrow alley framing distant landmark"
    ],
    narrative_themes=[
        "layers of history in stone", "old world charm endures",
        "craftsmanship across centuries", "public squares as living rooms",
        "secrets of narrow passages", "faith expressed in architecture",
        "the evening promenade", "markets and merchants through ages",
        "fortress becomes home", "beauty built to last"
    ]
)

# Domain 17: Japanese Beauty
japanese_beauty = Domain(
    name="Japanese Natural & Cultural Beauty",
    icon="🗾",
    description="Classical Japanese buildings, agricultural fields, cherry blossoms, and natural serenity",
    locations=[
        "Cherry blossom grove in full bloom", "Traditional wooden temple complex",
        "Rice paddy fields reflecting sky", "Japanese strolling garden with pond",
        "Arashiyama bamboo forest path", "Tea house with tatami and shoji screens",
        "Mount Fuji vista across lake", "Floating torii gate at water's edge",
        "Zen rock garden with raked gravel patterns", "Mountain onsen with steam rising",
        "Wisteria tunnel in purple cascade", "Shinto shrine with vermillion gates",
        "Thatched roof farmhouse in valley", "Moss garden with centuries of growth",
        "Autumn maple garden with stone lanterns", "Koi pond with arched bridge",
        "Snow-covered temple in Kyoto", "Fishing village with traditional boats",
        "Terraced tea plantation with mist", "Night illumination of autumn leaves",
        "Dry landscape garden at Ryoan-ji", "Plum blossom grove in early spring",
        "Mountain waterfall at sacred site", "Traditional street in Gion district",
        "Island shrine connected by bridge", "Firefly river in summer night"
    ],
    signature_elements=[
        "cherry blossoms (sakura) in pink clouds", "vermillion torii gates in rows",
        "traditional curved temple rooflines", "carefully pruned bonsai and garden trees",
        "koi fish in crystal clear ponds", "stone lanterns (toro) with moss",
        "tatami rooms with ikebana arrangement", "flooded rice paddies mirroring sky",
        "red maple leaves (momiji)", "bamboo grove with filtered light",
        "shoji screen with soft light behind", "zen raked gravel circles and lines",
        "wisteria hanging in cascades", "wooden bridge over garden stream",
        "stone water basin (tsukubai)", "paper lanterns glowing at night",
        "crane standing in shallow water", "moss on everything ancient",
        "cedar bark temple walls", "steam from volcanic hot spring",
        "wind chime (furin) in breeze", "snow on stone Buddha",
        "autumn leaves floating on water", "traditional indigo fabric drying",
        "fireflies over summer stream"
    ],
    lighting_conditions=[
        "soft spring light through blossoms", "golden autumn maple glow",
        "misty morning on rice fields", "zen garden in calm overcast",
        "lantern light at twilight temple", "snow-reflected soft winter light",
        "summer green filtered through bamboo", "moonlight on a still garden pond"
    ],
    camera_weights={"pan_right": 0.3, "zoom_in": 0.25, "tilt_up": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["cherry blossom pink", "zen green", "red shrine", "natural wood"],
    mood_keywords=["serene", "harmonious", "peaceful", "elegant", "traditional", "refined", "contemplative", "ephemeral"],
    style_prompt="Japanese landscape, traditional architecture, natural beauty, zen atmosphere",
    time_periods=[
        "pre-dawn temple bell sounds", "sunrise on Mount Fuji",
        "golden hour on temple roofs", "noon harsh but clear",
        "late afternoon tea ceremony light", "blue hour with paper lanterns",
        "twilight firefly time", "midnight zen garden meditation",
        "dawn mist on rice paddies"
    ],
    seasons=[
        "cherry blossom season (hanami)", "fresh green season (shinryoku)",
        "rainy season (tsuyu) with hydrangeas", "summer matsuri festivals",
        "autumn leaf viewing (koyo)", "first snow on temples (hatsu-yuki)",
        "deep winter contemplation", "plum blossom early spring (ume)"
    ],
    weather_conditions=[
        "cherry blossom rain (hanafubuki)", "light spring drizzle",
        "summer humidity with cicada sounds", "autumn clarity after typhoon",
        "first snow gently falling", "mist rising from hot springs",
        "rainy season steady warm rain", "crisp winter morning with frost",
        "wind scattering autumn leaves"
    ],
    perspectives=[
        "aerial drone over temple complex", "from engawa porch at garden",
        "macro close-up of blossom detail", "through shoji screen frame",
        "reflection in garden pond", "looking up through bamboo canopy",
        "along stone path perspective", "from tea room through small window",
        "across rice paddy to mountains", "from torii gate toward shrine"
    ],
    narrative_themes=[
        "wabi-sabi imperfect beauty", "mono no aware (pathos of things)",
        "ma (negative space as presence)", "seasons as life metaphor",
        "craft and devotion", "nature and architecture as one",
        "the way of tea (tranquility)", "cherry blossom impermanence",
        "garden as miniature universe", "stillness in motion"
    ]
)

# Domain 18: Amazon Rainforest
amazon_rainforest = Domain(
    name="Amazon Rainforest Beauty",
    icon="🦜",
    description="Wild jungle beauty with rivers, biodiversity, and untamed natural splendor",
    locations=[
        "Wide river bend through dense jungle", "Canopy walkway 40 meters up",
        "Jungle floor with buttress roots", "Multi-tiered waterfall in remote forest",
        "Strangler fig tree hollow", "Wildlife habitat at clay lick",
        "Muddy riverbank with caiman tracks", "Dense vegetation wall at forest edge",
        "Ancient kapok tree reaching emergent layer", "Oxbow lake with giant water lilies",
        "Flooded forest (igapó) in high water season", "Piranha-filled tributary",
        "Indigenous village clearing", "River dolphin habitat at confluence",
        "Epiphyte garden on single tree branch", "Night jungle with glowing eyes",
        "Monkey troop crossing between trees", "Army ant column on forest floor",
        "Medicinal plant garden", "River rapids between boulders",
        "Toucan nesting tree", "Bromeliad-covered cloud forest slope",
        "Freshwater spring in jungle", "Howler monkey territory at dawn",
        "Jaguar trail along riverbank", "Orchid-covered fallen tree"
    ],
    signature_elements=[
        "dense multi-layered canopy", "scarlet macaws in flight", "pink river dolphins surfacing",
        "exotic heliconia flowers", "thick woody jungle vines", "massive buttress-rooted trees",
        "poison dart frogs in vivid color", "blue morpho butterflies", "misty atmosphere in layers",
        "howler monkeys calling", "sloth moving in slow motion", "toucan with enormous bill",
        "caiman eyes above water", "army ants in massive column", "giant water lily pads",
        "anaconda coiled on branch", "leafcutter ants carrying pieces", "bird of paradise plant",
        "tree frog on red-eyed leaf", "spider monkey swinging",
        "piranha teeth detail", "jaguar print in mud", "bioluminescent fungi at night",
        "hummingbird at flower", "capybara family at water's edge"
    ],
    lighting_conditions=[
        "dappled jungle light through canopy gaps", "early morning mist with green filter",
        "filtered sunbeams in cathedral-like forest", "twilight green understorey glow",
        "overcast humid diffused light", "river reflection doubling the green",
        "bioluminescent forest floor at night", "golden break in clouds over canopy"
    ],
    camera_weights={"zoom_in": 0.3, "tilt_up": 0.25, "pan_right": 0.2, "zoom_out": 0.15, "pan_left": 0.1},
    color_palette=["jungle green", "tropical blue", "earth brown", "vibrant wildlife colors"],
    mood_keywords=["wild", "mysterious", "vibrant", "primordial", "untamed", "alive", "dense", "ancient"],
    style_prompt="Amazon rainforest, jungle cinematography, tropical biodiversity",
    time_periods=[
        "pre-dawn with howler monkey alarm", "sunrise filtering through canopy",
        "golden hour on river surface", "harsh noon on canopy top only",
        "afternoon rainstorm", "blue hour with insects emerging",
        "twilight with bat flight", "midnight jungle alive with sound",
        "dawn chorus of birds"
    ],
    seasons=[
        "high water flooded forest season", "low water exposed riverbanks",
        "dry season with concentrated wildlife", "wet season green explosion",
        "fruiting season attracting animals", "breeding season with displays",
        "migration season for birds", "mushroom flush after heavy rains"
    ],
    weather_conditions=[
        "morning mist in river valley", "tropical downpour",
        "clearing after storm with steam", "humid still air",
        "light rain pattering on leaves", "dry spell with dust",
        "thunderstorm with lightning over canopy", "fog in cloud forest",
        "rainbow through waterfall spray"
    ],
    perspectives=[
        "aerial drone above canopy sea", "forest floor among roots",
        "macro close-up of insect detail", "from canopy walkway",
        "water level in flooded forest", "from river boat looking at bank",
        "inside hollow tree looking up", "eye level with monkey in tree",
        "from under giant lily pad", "night vision perspective"
    ],
    narrative_themes=[
        "the lungs of the Earth", "biodiversity in every square meter",
        "predator and prey in balance", "water as highway",
        "layers of life stacked vertical", "ancient ecosystem unchanged",
        "the jungle never sleeps", "adaptation and survival",
        "hidden worlds in miniature", "the river connects all"
    ]
)

# Domain 19: Beautiful Beaches
beautiful_beaches = Domain(
    name="Beautiful Beaches Worldwide",
    icon="🏖️",
    description="Stunning coastal paradises with white sand, turquoise water, and tropical beauty",
    locations=[
        "White sand beach with turquoise shallows", "Palm-lined shore with gentle waves",
        "Rocky cove with crystal clear water", "Beach sunset with silhouetted palms",
        "Tide pools with miniature sea life", "Sand dunes with beach grass waving",
        "Overwater bungalow beach resort", "Dramatic sea cliffs above beach",
        "Tropical lagoon with sandbars", "Black sand volcanic beach",
        "Pink sand beach from coral fragments", "Bioluminescent shore at night",
        "Secluded beach accessible only by boat", "Beach with massive boulders (Seychelles-style)",
        "Mangrove-fringed beach with clear water", "Beach cave with ocean view",
        "Endless beach stretching to vanishing point", "Coral beach with snorkeling from shore",
        "Beach hammock between leaning palms", "Tidal flat at low tide with patterns",
        "Surfing beach with perfect wave line", "Fishing beach with colorful boats",
        "Cliff-backed beach with waterfall to sand", "Sandcastle territory on wide beach",
        "Lighthouse beach with dramatic headland", "Shell beach covered in thousands of shells"
    ],
    signature_elements=[
        "powder white sand between toes", "turquoise water in gradients of blue",
        "coconut palm trees leaning over water", "beach umbrella and sun chairs",
        "gentle waves with white foam", "seashells scattered on wet sand",
        "driftwood shaped by ocean", "golden sunset over water",
        "crystal clear water showing sandy bottom", "footprints in fresh sand",
        "starfish on shore", "beach bonfire at dusk",
        "tropical flowers on sand", "hermit crab crossing beach",
        "pelican diving for fish", "sailing boat on horizon",
        "tide line with seaweed and shells", "sand patterns from receding waves",
        "coral pieces on beach", "coconut on shore", "sea glass in sand",
        "beach grass in wind", "hammock swinging gently",
        "snorkel mask and fins on sand", "message in a bottle concept"
    ],
    lighting_conditions=[
        "bright beach sun with sparkling water", "golden sunset painting everything amber",
        "soft early morning before crowds", "blue hour with gentle ocean glow",
        "midday tropical light with vivid colors", "bioluminescent beach at night",
        "overcast creating soft even light", "sunrise behind palm silhouettes"
    ],
    camera_weights={"pan_right": 0.3, "zoom_out": 0.25, "zoom_in": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["turquoise", "white sand", "sunset orange", "sky blue"],
    mood_keywords=["relaxing", "tropical", "paradise", "peaceful", "idyllic", "blissful", "warm", "carefree"],
    style_prompt="beach cinematography, tropical paradise, coastal beauty",
    time_periods=[
        "pre-dawn with stars over ocean", "sunrise lighting clouds from below",
        "golden hour with long shadows on sand", "noon with overhead sun and vivid water",
        "late afternoon warm glow", "blue hour with smooth ocean",
        "sunset with sky on fire", "moonrise over ocean",
        "midnight bioluminescence"
    ],
    seasons=[
        "peak tropical dry season", "monsoon dramatic skies and surf",
        "turtle nesting season", "whale watching season from shore",
        "summer crowded and lively", "winter quiet and pristine",
        "spring with migrating birds", "autumn with warm water cool breeze"
    ],
    weather_conditions=[
        "perfectly clear tropical day", "light tropical shower with sun",
        "dramatic clouds with rays breaking through", "calm glassy morning water",
        "onshore breeze with small surf", "post-storm with dramatic sky and big waves",
        "heat haze on beach", "gentle fog lifting at dawn",
        "rainbow over ocean"
    ],
    perspectives=[
        "aerial drone over beach and reef", "water level half submerged",
        "macro close-up of sand patterns", "through palm frond frame",
        "from hammock looking at ocean", "underwater looking at beach from sea",
        "from cliff above looking down", "walking perspective along tide line",
        "from beach cave looking out", "drone pulling back from close to wide"
    ],
    narrative_themes=[
        "paradise found", "where land meets sea",
        "footprints washed away", "eternal summer",
        "the simplicity of sand and water", "tides as time keeper",
        "solitude on shore", "colors of the coast",
        "beach as equalizer", "horizon as possibility"
    ]
)

# Domain 20: Luxury Palace Interiors
luxury_palace = Domain(
    name="Luxury Palace Interiors",
    icon="👑",
    description="Opulent royal interiors with grand furnishings, chandeliers, and baroque elegance",
    locations=[
        "Grand ballroom with parquet floor", "Throne room with canopy and carpet",
        "Royal library with floor-to-ceiling books", "Music room with grand piano and harp",
        "State dining hall with 40-seat table", "Game room with snooker and chess",
        "Master bedroom with four-poster bed", "Portrait gallery with gilded frames",
        "Private study with writing desk", "Chapel with painted ceiling",
        "Orangery with potted citrus trees", "Mirror gallery reflecting chandeliers",
        "Marble entrance hall with double staircase", "Dressing room with jewelry displays",
        "Conservatory with stained glass dome", "Wine cellar with vaulted brick ceiling",
        "Drawing room with silk wallpaper", "Armory with displayed weapons and armor",
        "Kitchen with copper pots and stone hearth", "Observatory tower with telescope",
        "Royal bathroom with marble tub", "Servants' corridor behind walls",
        "Garden terrace with palace facade behind", "Ballroom balcony overlooking dance floor",
        "Secret passage revealed behind bookcase", "Crown jewel display room"
    ],
    signature_elements=[
        "crystal chandeliers with hundreds of prisms", "grand piano reflecting candlelight",
        "velvet sofas in jewel tones", "snooker table with green baize",
        "throne chairs with carved arms", "polished marble floors with inlay patterns",
        "gold leaf accents everywhere", "tapestries depicting historical scenes",
        "ornate mirrors multiplying space", "silk curtains with tassel tiebacks",
        "porcelain vases on pedestals", "painted ceiling with clouds and angels",
        "carved wooden panels and wainscoting", "candelabra with dripping wax",
        "Persian rugs on marble floors", "grandfather clock with gilt face",
        "crystal decanters with amber liquid", "fresh flower arrangements towering",
        "silver service on buffet", "gilded picture frames in ornate patterns",
        "bust sculpture on column", "hand-painted wallpaper with birds",
        "fireplace mantel with carved figures", "stained glass window casting colors",
        "crown molding and ceiling rosettes"
    ],
    lighting_conditions=[
        "golden chandelier glow filling ballroom", "natural window light through tall french doors",
        "candlelit ambience with warm flicker", "sunset through stained glass windows",
        "morning light in portrait gallery", "fireplace glow in study",
        "moonlight through conservatory glass", "dramatic spotlight on throne"
    ],
    camera_weights={"zoom_in": 0.3, "pan_right": 0.25, "zoom_out": 0.2, "pan_left": 0.15, "tilt_up": 0.1},
    color_palette=["royal gold", "marble white", "velvet red", "ornate bronze"],
    mood_keywords=["opulent", "royal", "majestic", "elegant", "sophisticated", "grandiose", "regal", "sumptuous"],
    style_prompt="palace interior, royal luxury, baroque architecture, opulent furnishings",
    time_periods=[
        "dawn light entering through tall windows", "morning with dust motes in sunbeams",
        "golden hour warming gilded surfaces", "noon with sharp shadows in corridors",
        "afternoon tea in drawing room", "blue hour with chandeliers lit",
        "candlelit evening banquet", "midnight with single candle in corridor",
        "ball in full swing with all lights blazing"
    ],
    seasons=[
        "winter ball season with roaring fires", "spring with fresh flowers everywhere",
        "summer with doors open to gardens", "autumn with tapestry colors echoed outside",
        "Christmas with decorated great hall", "harvest feast in dining hall",
        "coronation ceremony setup", "summer solstice garden party extending inside"
    ],
    weather_conditions=[
        "rain streaming down tall windows", "sunlight flooding through glass dome",
        "overcast giving soft museum-like light", "storm with lightning illuminating room",
        "snow visible through frosted windows", "warm evening with open terrace doors",
        "fog pressing against windows", "clear day with garden reflected in mirrors"
    ],
    perspectives=[
        "aerial view of ballroom from ceiling", "ground level along marble floor",
        "macro close-up of gilt detail", "through doorway into next grand room",
        "reflection in enormous mirror", "looking up at painted ceiling",
        "from throne at approaching visitors", "down grand staircase",
        "through keyhole into secret room", "from balcony at room below"
    ],
    narrative_themes=[
        "power expressed in beauty", "centuries of accumulated wealth",
        "the palace as stage", "craftsmanship elevated to art",
        "private moments in public spaces", "the weight of the crown",
        "elegance as daily life", "secrets behind gilded doors",
        "the palace remembers everything", "grandeur and intimacy coexist"
    ]
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
