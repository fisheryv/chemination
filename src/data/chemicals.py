"""Chemical enemy database for the Chemination game.

This module contains the database of enemy chemicals, organized by type
(acids, bases, salts, and metals). Each enemy has specific properties
like health points and movement speed.
"""

# Enemy (chemical formula) database
ENEMIES = {
    # Acids
    "HCl": {
        "type": "acid",
        "hp": 3,
        "speed": 5,
    },
    "H2SO4": {
        "type": "acid",
        "hp": 4,
        "speed": 3,
    },
    "HNO3": {
        "type": "acid",
        "hp": 4,
        "speed": 3,
    },
    "HF": {
        "type": "acid",
        "hp": 2,
        "speed": 5,
    },
    "H3PO4": {
        "type": "acid",
        "hp": 2,
        "speed": 2,
    },
    "H2CO3": {
        "type": "acid",
        "hp": 1,
        "speed": 3,
    },
    "HS": {
        "type": "acid",
        "hp": 2,
        "speed": 5,
    },
    "CH3COOH": {
        "type": "acid",
        "hp": 1,
        "speed": 2,
    },
    
    # Bases
    "NaOH": {
        "type": "base",
        "hp": 4,
        "speed": 5,
    },
    "KOH": {
        "type": "base",
        "hp": 4,
        "speed": 5,
    },
    "Ca(OH)2": {
        "type": "base",
        "hp": 3,
        "speed": 3,
    },
    "Ba(OH)2": {
        "type": "base",
        "hp": 3,
        "speed": 3,
    },
    "Mg(OH)2": {
        "type": "base",
        "hp": 2,
        "speed": 4,
    },
    "NH3·H2O": {
        "type": "base",
        "hp": 1,
        "speed": 4,
    },
    
    # Salts
    "CuSO4": {
        "type": "salt",
        "hp": 3,
        "speed": 2,
    },
    "AgNO3": {
        "type": "salt",
        "hp": 4,
        "speed": 3,
    },
    "BaCl2": {
        "type": "salt",
        "hp": 4,
        "speed": 2,
    },
    
    # Metals
    "Au": {
        "type": "metal",
        "hp": 10,
        "speed": 1,
    },
    "Fe": {
        "type": "metal",
        "hp": 6,
        "speed": 2,
    },
    "Cu": {
        "type": "metal",
        "hp": 5,
        "speed": 2,
    }
}

# Enemy grouping (for displaying enemy information in help interface)
ENEMIES_SPIRIT = {
    # Acids - Row 1
    "a1": ["HCl", "H2SO4", "HNO3", "HF"],
    # Acids - Row 2
    "a2": ["H3PO4", "H2CO3", "HS", "CH3COOH"],
    # Bases - Row 1
    "b1": ["NaOH", "KOH", "Ca(OH)2"],
    # Bases - Row 2
    "b2": ["Ba(OH)2", "Mg(OH)2", "NH3·H2O"],
    # Salts
    "s": ["CuSO4", "AgNO3", "BaCl2"],
    # Metals
    "m": ["Au", "Fe", "Cu"]
}