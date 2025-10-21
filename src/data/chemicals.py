# 敌人（化学式）数据库
ENEMIES = {
    # 酸类
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
    
    # 碱类
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
    
    # 盐类
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
    
    # 金属类
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

# 敌人分组（用于帮助界面展示敌人信息）
ENEMIES_SPIRIT = {
    # 酸类 - 第一行
    "a1": ["HCl", "H2SO4", "HNO3", "HF"],
    # 酸类 - 第二行
    "a2": ["H3PO4", "H2CO3", "HS", "CH3COOH"],
    # 碱类 - 第一行
    "b1": ["NaOH", "KOH", "Ca(OH)2"],
    # 碱类 - 第二行
    "b2": ["Ba(OH)2", "Mg(OH)2", "NH3·H2O"],
    # 盐类
    "s": ["CuSO4", "AgNO3", "BaCl2"],
    # 金属类
    "m": ["Au", "Fe", "Cu"]
}
