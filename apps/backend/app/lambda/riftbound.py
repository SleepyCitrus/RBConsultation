# Game name
RIFTBOUND = "riftbound-league-of-legends-trading-card-game"

# Colors
RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
PURPLE = "purple"

# Sets
ORIGINS = "origins"
SPIRITFORGED = "spiritforged"
UNLEASHED = "unleashed"
VENDETTA = "vendetta"

# Rarity
COMMON = "common"
UNCOMMON = "uncommon"
RARE = "rare"
EPIC = "epic"
SHOWCASE = "showcase"

# Printing
NORMAL = "Normal"
FOIL = "Foil"

# Condition
NEAR_MINT = "Near Mint"


class StapleCard:
    def __init__(self, name: str, set: str, rarity: str, color: str, tcgplayer_id: int = 0):
        self.name = name
        self.set = set
        self.rarity = rarity
        self.color = color
        if rarity in [COMMON, UNCOMMON]:
            self.printing = NORMAL
        else:
            self.printing = FOIL
        self.tcgplayer_id = tcgplayer_id # Optional, mostly used for searches

def get_card_slug(card_name: str, card_set: str, rarity: str) -> str:
    """
    Get the slug for a card given its name.
    """
    slug = []

    slug.append(RIFTBOUND)
    slug.append(card_set)
    slug.append(card_name.lower().replace(" ", "-").replace(",'", ""))
    slug.append(rarity)

    return "-".join(slug)

def _get_staples() -> list[StapleCard]:
    """
    Get a list of staple cards for Riftbound.
    """
    # Total is 60 cards as of 8/18/26

    return [
        # Seals - 6
        StapleCard(name="Seal of Rage", set=ORIGINS, rarity=EPIC, color=RED, tcgplayer_id=652814),  # CHECK
        StapleCard(name="Seal of Strength", set=ORIGINS, rarity=EPIC, color=ORANGE, tcgplayer_id=652950),  # CHECK
        StapleCard(name="Seal of Unity", set=ORIGINS, rarity=EPIC, color=YELLOW, tcgplayer_id=653042),  # CHECK
        StapleCard(name="Seal of Focus", set=ORIGINS, rarity=EPIC, color=GREEN, tcgplayer_id=652861),  # CHECK
        StapleCard(name="Seal of Insight", set=ORIGINS, rarity=EPIC, color=BLUE, tcgplayer_id=652902),  # CHECK
        StapleCard(name="Seal of Discord", set=ORIGINS, rarity=EPIC, color=PURPLE, tcgplayer_id=652996),  # CHECK

        # Red - 7
        StapleCard(name="Falling Star", set=ORIGINS, rarity=RARE, color=RED, tcgplayer_id=652801),
        StapleCard(name="Ferrous Forerunner", set=SPIRITFORGED, rarity=RARE, color=RED, tcgplayer_id=666364),
        StapleCard(name="Kai'Sa, Survivor", set=ORIGINS, rarity=EPIC, color=RED, tcgplayer_id=652812), # CHECK
        StapleCard(name="Darius, Trifarian", set=ORIGINS, rarity=RARE, color=RED, tcgplayer_id=652798),
        StapleCard(name="Pyke, Dockside Butcher", set=UNLEASHED, rarity=EPIC, color=RED, tcgplayer_id=685003),
        StapleCard(name="Rek'Sai, Breacher", set=SPIRITFORGED, rarity=EPIC, color=RED, tcgplayer_id=666493),
        StapleCard(name="Immortal Phoenix", set=ORIGINS, rarity=EPIC, color=RED, tcgplayer_id=652810),

        # Orange - 7
        StapleCard(name="Sabotage", set=ORIGINS, rarity=RARE, color=ORANGE, tcgplayer_id=652941),
        StapleCard(name="Rengar, Trophy Hunter", set=UNLEASHED, rarity=EPIC, color=ORANGE, tcgplayer_id=684215),
        StapleCard(name="Akshan, Mischievous", set=SPIRITFORGED, rarity=RARE, color=ORANGE, tcgplayer_id=666888),
        StapleCard(name="Irresistible Faefolk", set=UNLEASHED, rarity=RARE, color=ORANGE, tcgplayer_id=686325),
        StapleCard(name="Elder Dragon", set=UNLEASHED, rarity=EPIC, color=ORANGE, tcgplayer_id=685007),
        StapleCard(name="Dazzling Aurora", set=ORIGINS, rarity=EPIC, color=ORANGE, tcgplayer_id=652946),
        StapleCard(name="Sett, Brawler", set=ORIGINS, rarity=EPIC, color=ORANGE, tcgplayer_id=652951),

        # Yellow - 8
        StapleCard(name="Salvage", set=ORIGINS, rarity=UNCOMMON, color=YELLOW, tcgplayer_id=653018),
        StapleCard(name="Vi, Peacekeeper", set=UNLEASHED, rarity=EPIC, color=YELLOW, tcgplayer_id=685595),
        StapleCard(name="Sacrifice", set=UNLEASHED, rarity=RARE, color=YELLOW, tcgplayer_id=684479),
        StapleCard(name="Divine Judgment", set=ORIGINS, rarity=EPIC, color=YELLOW, tcgplayer_id=653041),
        StapleCard(name="Azir, Sovereign", set=SPIRITFORGED, rarity=EPIC, color=YELLOW, tcgplayer_id=666473),
        StapleCard(name="Baited Hook", set=ORIGINS, rarity=EPIC, color=YELLOW, tcgplayer_id=653038),
        StapleCard(name="Rift Herald", set=UNLEASHED, rarity=EPIC, color=YELLOW, tcgplayer_id=684546),
        StapleCard(name="The Ruination", set=UNLEASHED, rarity=EPIC, color=YELLOW, tcgplayer_id=685492),

        # Green - 10
        StapleCard(name="Defy", set=ORIGINS, rarity=COMMON, color=GREEN, tcgplayer_id=652821),
        StapleCard(name="Discipline", set=ORIGINS, rarity=UNCOMMON, color=GREEN, tcgplayer_id=652834),  # CHECK
        StapleCard(name="Scuttle Crab", set=UNLEASHED, rarity=RARE, color=GREEN, tcgplayer_id=685519),  # CHECK
        StapleCard(name="En Garde", set=ORIGINS, rarity=COMMON, color=GREEN, tcgplayer_id=652822),
        StapleCard(name="Zhonya's Hourglass", set=ORIGINS, rarity=RARE, color=GREEN, tcgplayer_id=652855),
        StapleCard(name="Not So Fast", set=SPIRITFORGED, rarity=UNCOMMON, color=GREEN, tcgplayer_id=665592),
        StapleCard(name="Stellacorn Herder", set=SPIRITFORGED, rarity=COMMON, color=GREEN, tcgplayer_id=665141),
        StapleCard(name="Guardian Angel", set=SPIRITFORGED, rarity=RARE, color=GREEN, tcgplayer_id=663435),
        StapleCard(name="Irelia, Fervent", set=SPIRITFORGED, rarity=EPIC, color=GREEN, tcgplayer_id=664885),  # CHECK
        StapleCard(name="Vilemaw", set=UNLEASHED, rarity=EPIC, color=GREEN, tcgplayer_id=684125),

        # Blue - 9
        StapleCard(name="Thousand-Tailed Watcher", set=ORIGINS, rarity=RARE, color=BLUE, tcgplayer_id=652898),
        StapleCard(name="Bellows Breath", set=SPIRITFORGED, rarity=RARE, color=BLUE, tcgplayer_id=665009),
        StapleCard(name="Sprite Fountain", set=UNLEASHED, rarity=UNCOMMON, color=BLUE, tcgplayer_id=685589),
        StapleCard(name="Time Warp", set=ORIGINS, rarity=EPIC, color=BLUE, tcgplayer_id=652905),
        StapleCard(name="Unchecked Power", set=ORIGINS, rarity=EPIC, color=BLUE, tcgplayer_id=652906),
        StapleCard(name="Mel, Newly Awakened", set=VENDETTA, rarity=EPIC, color=BLUE, tcgplayer_id=706064),
        StapleCard(name="Progress Day", set=ORIGINS, rarity=RARE, color=BLUE, tcgplayer_id=652896),
        StapleCard(name="Hwei, Brooding Painter", set=UNLEASHED, rarity=RARE, color=BLUE, tcgplayer_id=684474),
        StapleCard(name="Premonition", set=SPIRITFORGED, rarity=EPIC, color=BLUE, tcgplayer_id=665014),

        # Purple - 13
        StapleCard(name="Stacked Deck", set=ORIGINS, rarity=UNCOMMON, color=PURPLE, tcgplayer_id=652972),
        StapleCard(name="Fizz, Trickster", set=SPIRITFORGED, rarity=RARE, color=PURPLE, tcgplayer_id=666489),
        StapleCard(name="Tideturner", set=ORIGINS, rarity=RARE, color=PURPLE, tcgplayer_id=652990),
        StapleCard(name="Vex, Apathetic", set=UNLEASHED, rarity=EPIC, color=PURPLE, tcgplayer_id=685949),
        StapleCard(name="Kennen, Storm of Shuriken", set=VENDETTA, rarity=UNCOMMON, color=PURPLE, tcgplayer_id=706051),
        StapleCard(name="Last Rites", set=SPIRITFORGED, rarity=EPIC, color=PURPLE, tcgplayer_id=665029),
        StapleCard(name="Baron Nashor", set=UNLEASHED, rarity=EPIC, color=PURPLE, tcgplayer_id=683790),
        StapleCard(name="Invert Timelines", set=ORIGINS, rarity=EPIC, color=PURPLE, tcgplayer_id=652992),
        StapleCard(name="Rhasa the Sunderer", set=ORIGINS, rarity=RARE, color=PURPLE, tcgplayer_id=652985),
        StapleCard(name="Nocturne, Horrifying", set=ORIGINS, rarity=RARE, color=PURPLE, tcgplayer_id=652984),
        StapleCard(name="Pyke, Returned", set=UNLEASHED, rarity=RARE, color=PURPLE, tcgplayer_id=684509),
        StapleCard(name="Downwell", set=SPIRITFORGED, rarity=EPIC, color=PURPLE, tcgplayer_id=666477),
        StapleCard(name="Ezreal, Prodigy", set=SPIRITFORGED, rarity=EPIC, color=PURPLE, tcgplayer_id=666825),
    ]

def get_staple_cards_dict() -> dict[str, StapleCard]:
    staple_dict = {}
    for staple in _get_staples():
        slug = get_card_slug(staple.name, staple.set, staple.rarity)
        staple_dict[slug] = staple
    return staple_dict

