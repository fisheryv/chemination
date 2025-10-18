import random

# 化学式数据库
# 酸类 - 常见无机酸和有机酸
ACIDS = [
    # 常见无机强酸
    'HCl',      # 盐酸
    'H2SO4',    # 硫酸
    'HNO3',     # 硝酸
    'HClO4',    # 高氯酸
    'HBr',      # 氢溴酸
    'HI',       # 氢碘酸
    
    # 中强酸
    'H3PO4',    # 磷酸
    'HF',       # 氢氟酸
    'HNO2',     # 亚硝酸
    'H2SO3',    # 亚硫酸
    
    # 弱酸
    'H2CO3',    # 碳酸
    'H2S',      # 硫化氢
    'HClO',     # 次氯酸
    'H2SiO3',   # 硅酸
    
    # 有机酸
    'CH3COOH',  # 乙酸（醋酸）
]

# 碱类 - 常见无机碱
BASES = [
    # 强碱
    'NaOH',     # 氢氧化钠
    'KOH',      # 氢氧化钾
    'Ca(OH)2',  # 氢氧化钙
    'Ba(OH)2',  # 氢氧化钡
    
    # 中强碱和弱碱
    'Mg(OH)2',  # 氢氧化镁
    'NH3·H2O',  # 氨水
    'Al(OH)3',  # 氢氧化铝
    'Fe(OH)2',  # 氢氧化亚铁
    'Fe(OH)3',  # 氢氧化铁
    'Cu(OH)2',  # 氢氧化铜
    'Zn(OH)2',  # 氢氧化锌
    'Pb(OH)2',  # 氢氧化铅
    'Ni(OH)2',  # 氢氧化镍
    'Co(OH)2',  # 氢氧化钴
    'Mn(OH)2',  # 氢氧化锰
    'Cr(OH)3',  # 氢氧化铬
]

# 盐类 - 各种类型的盐
SALTS = [
    # 氯化物
    'NaCl',     # 氯化钠
    'KCl',      # 氯化钾
    'CaCl2',    # 氯化钙
    'MgCl2',    # 氯化镁
    'AlCl3',    # 氯化铝
    'FeCl2',    # 氯化亚铁
    'FeCl3',    # 氯化铁
    'CuCl2',    # 氯化铜
    'ZnCl2',    # 氯化锌
    'AgCl',     # 氯化银
    'NH4Cl',    # 氯化铵
    'BaCl2',    # 氯化钡
    
    # 硫酸盐
    'Na2SO4',   # 硫酸钠
    'K2SO4',    # 硫酸钾
    'CaSO4',    # 硫酸钙
    'MgSO4',    # 硫酸镁
    'Al2(SO4)3',# 硫酸铝
    'FeSO4',    # 硫酸亚铁
    'Fe2(SO4)3',# 硫酸铁
    'CuSO4',    # 硫酸铜
    'ZnSO4',    # 硫酸锌
    'BaSO4',    # 硫酸钡
    '(NH4)2SO4',# 硫酸铵
    
    # 硝酸盐
    'NaNO3',    # 硝酸钠
    'KNO3',     # 硝酸钾
    'Ca(NO3)2', # 硝酸钙
    'Mg(NO3)2', # 硝酸镁
    'Al(NO3)3', # 硝酸铝
    'Fe(NO3)2', # 硝酸亚铁
    'Fe(NO3)3', # 硝酸铁
    'Cu(NO3)2', # 硝酸铜
    'AgNO3',    # 硝酸银
    'Zn(NO3)2', # 硝酸锌
    'Pb(NO3)2', # 硝酸铅
    'NH4NO3',   # 硝酸铵
    
    # 碳酸盐
    'Na2CO3',   # 碳酸钠
    'K2CO3',    # 碳酸钾
    'CaCO3',    # 碳酸钙
    'MgCO3',    # 碳酸镁
    'FeCO3',    # 碳酸亚铁
    'BaCO3',    # 碳酸钡
    'Li2CO3',   # 碳酸锂
    '(NH4)2CO3',# 碳酸铵
    
    # 碳酸氢盐
    'NaHCO3',   # 碳酸氢钠
    'KHCO3',    # 碳酸氢钾
    'Ca(HCO3)2',# 碳酸氢钙
    'Mg(HCO3)2',# 碳酸氢镁
    'NH4HCO3',  # 碳酸氢铵
    
    # 磷酸盐
    'Na3PO4',   # 磷酸钠
    'K3PO4',    # 磷酸钾
    'Ca3(PO4)2',# 磷酸钙
    'Na2HPO4',  # 磷酸氢二钠
    'NaH2PO4',  # 磷酸二氢钠
    '(NH4)3PO4',# 磷酸铵
    
    # 亚硫酸盐
    'Na2SO3',   # 亚硫酸钠
    'K2SO3',    # 亚硫酸钾
    'CaSO3',    # 亚硫酸钙
    
    # 卤化物（其他）
    'NaBr',    # 卤化物（其他）
    'NaBr',     # 溴化钠
    'KBr',      # 溴化钾
    'CaBr2',    # 溴化钙
    'MgBr2',    # 溴化镁
    'NaI',      # 碘化钠
    'KI',       # 碘化钾
    'CaI2',     # 碘化钙
    'AgBr',     # 溴化银
    'AgI',      # 碘化银
    'NaF',      # 氟化钠
    'KF',       # 氟化钾
    'CaF2',     # 氟化钙
    
    # 硫化物
    'Na2S',     # 硫化钠
    'K2S',      # 硫化钾
    'CaS',      # 硫化钙
    'MgS',      # 硫化镁
    'FeS',      # 硫化亚铁
    'FeS2',     # 二硫化铁
    'CuS',      # 硫化铜
    'Cu2S',     # 硫化亚铜
    'ZnS',      # 硫化锌
    'PbS',      # 硫化铅
    'Ag2S',     # 硫化银
    'HgS',      # 硫化汞
    
    # 氧化物盐
    'Na2O2',    # 过氧化钠
    'K2O2',     # 过氧化钾
    'BaO2',     # 过氧化钡
    
    # 铬酸盐
    'Na2CrO4',  # 铬酸钠
    'K2CrO4',   # 铬酸钾
    'K2Cr2O7',  # 重铬酸钾
    'PbCrO4',   # 铬酸铅
    
    # 高锰酸盐
    'KMnO4',    # 高锰酸钾
    'NaMnO4',   # 高锰酸钠
    'Ca(MnO4)2',# 高锰酸钙
    
    # 亚硝酸盐
    'NaNO2',    # 亚硝酸钠
    'KNO2',     # 亚硝酸钾
    
    # 氯酸盐
    'NaClO3',   # 氯酸钠
    'KClO3',    # 氯酸钾
    'Ca(ClO3)2',# 氯酸钙
    
    # 高氯酸盐
    'NaClO4',   # 高氯酸钠
    'KClO4',    # 高氯酸钾
    
    # 次氯酸盐
    'NaClO',    # 次氯酸钠
    'Ca(ClO)2', # 次氯酸钙
    
    # 硅酸盐
    'Na2SiO3',  # 硅酸钠
    'K2SiO3',   # 硅酸钾
    'CaSiO3',   # 硅酸钙
    
    # 醋酸盐
    'CH3COONa', # 醋酸钠
    'CH3COOK',  # 醋酸钾
    '(CH3COO)2Ca',# 醋酸钙
    '(CH3COO)2Mg',# 醋酸镁
    '(CH3COO)2Pb',# 醋酸铅
    '(CH3COO)2Cu',# 醋酸铜
    'CH3COONH4',# 醋酸铵

    # 复盐
    'KAl(SO4)2',# 硫酸铝钾
    'NH4Al(SO4)2',# 硫酸铝铵
    'NH4Fe(SO4)2',# 硫酸亚铁铵
    
    # 酸式盐
    'NaHSO4',   # 硫酸氢钠
    'KHSO4',    # 硫酸氢钾
    'NaHSO3',   # 亚硫酸氢钠
    'KHSO3',    # 亚硫酸氢钾
    'NaHS',     # 硫氢化钠
    'KHS',      # 硫氢化钾
    
    # 碱式盐
    'Cu2(OH)2CO3',# 碱式碳酸铜
    'Mg(OH)Cl', # 碱式氯化镁
    'Ca(OH)Cl', # 碱式氯化钙（漂白粉主要成分）
]

# 为了增加游戏难度，创建不同难度级别的化学式列表
EASY_ACIDS = ['HCl', 'H2SO4', 'HNO3', 'H2CO3', 'CH3COOH']
EASY_BASES = ['NaOH', 'KOH', 'Ca(OH)2', 'NH3·H2O', 'Ba(OH)2']
EASY_SALTS = ['NaCl', 'KCl', 'CaCO3', 'Na2CO3', 'CuSO4', 'FeSO4', 'KNO3']

MEDIUM_ACIDS = EASY_ACIDS + ['H3PO4', 'HF', 'HBr', 'HI', 'H2S', 'HCOOH', 'H2SO3']
MEDIUM_BASES = EASY_BASES + ['Al(OH)3', 'Fe(OH)3', 'Cu(OH)2', 'Mg(OH)2', 'Zn(OH)2']
MEDIUM_SALTS = EASY_SALTS + ['Al2(SO4)3', 'NH4Cl', 'Na2SO4', 'AgNO3', 'BaCl2', 'MgSO4']

HARD_ACIDS = ACIDS  # 使用所有酸
HARD_BASES = BASES  # 使用所有碱
HARD_SALTS = SALTS  # 使用所有盐

# 根据难度选择化学式库的函数
def get_formulas_by_difficulty(difficulty):
    """
    根据难度返回对应的化学式列表
    difficulty: 'easy', 'medium', 'hard', 'expert'
    """
    if difficulty == 'easy':
        return {
            'acids': EASY_ACIDS,
            'bases': EASY_BASES,
            'salts': EASY_SALTS
        }
    elif difficulty == 'medium':
        return {
            'acids': MEDIUM_ACIDS,
            'bases': MEDIUM_BASES,
            'salts': MEDIUM_SALTS
        }
    else:  # hard
        return {
            'acids': HARD_ACIDS,
            'bases': HARD_BASES,
            'salts': HARD_SALTS
        }
