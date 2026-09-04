# Game name
RIFTBOUND = "riftbound-league-of-legends-trading-card-game"

# Colors
RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
PURPLE = "purple"

# Set Labels
ORIGINS_LABEL = "origins"
SPIRITFORGED_LABEL = "spiritforged"
UNLEASHED_LABEL = "unleashed"
VENDETTA_LABEL = "vendetta"
RIFTBOUND_SET_LABELS = [
    ORIGINS_LABEL,
    SPIRITFORGED_LABEL,
    UNLEASHED_LABEL,
    VENDETTA_LABEL,
]
RIFTBOUND_SET_CAPITALIZED_LABELS = [s.capitalize() for s in RIFTBOUND_SET_LABELS]

# Set IDs
ORIGINS_ID = "ogn"
SPIRITFORGED_ID = "sfd"
UNLEASHED_ID = "unl"
VENDETTA_ID = "ven"
RIFTBOUND_SET_IDS = [ORIGINS_ID, SPIRITFORGED_ID, UNLEASHED_ID, VENDETTA_ID]

# Rarity
COMMON = "common"
UNCOMMON = "uncommon"
RARE = "rare"
EPIC = "epic"
SHOWCASE = "showcase"
SPECIAL_RARE = "sp"
OVERNUMBERED = "overnumbered"
SIGNATURE = "signature"
ULTIMATE = "ultimate"
RIFTBOUND_RARITY_LABELS = [
    COMMON,
    UNCOMMON,
    RARE,
    EPIC,
    SHOWCASE,
    SPECIAL_RARE,
    OVERNUMBERED,
    SIGNATURE,
    ULTIMATE,
]
RIFTBOUND_RARITY_CAPITALIZED_LABELS = [r.capitalize() for r in RIFTBOUND_RARITY_LABELS]

SHOWCASE_RARITY_TIERS = [SHOWCASE, SPECIAL_RARE, OVERNUMBERED, SIGNATURE, ULTIMATE]

# Types
BATTLEFIELD = "Battlefield"
GEAR = "Gear"
LEGEND = "Legend"
RUNE = "Rune"
SPELL = "Spell"
UNIT = "Unit"
