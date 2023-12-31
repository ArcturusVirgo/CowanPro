# ================================================
# 本文件用来存储与原子有关的信息
# ================================================
import json
from pathlib import Path


# 原子信息
ATOM = {1: ['H', '氢'], 2: ['He', '氦'], 3: ['Li', '锂'], 4: ['Be', '铍'], 5: ['B', '硼'],
        6: ['C', '碳'], 7: ['N', '氮'], 8: ['O', '氧'], 9: ['F', '氟'], 10: ['Ne', '氖'],
        11: ['Na', '钠'], 12: ['Mg', '镁'], 13: ['Al', '铝'], 14: ['Si', '硅'], 15: ['P', '磷'],
        16: ['S', '硫'], 17: ['Cl', '氯'], 18: ['Ar', '氩'], 19: ['K', '钾'], 20: ['Ca', '钙'],
        21: ['Sc', '钪'], 22: ['Ti', '钛'], 23: ['V', '钒'], 24: ['Cr', '铬'], 25: ['Mn', '锰'],
        26: ['Fe', '铁'], 27: ['Co', '钴'], 28: ['Ni', '镍'], 29: ['Cu', '铜'], 30: ['Zn', '锌'],
        31: ['Ga', '镓'], 32: ['Ge', '锗'], 33: ['As', '砷'], 34: ['Se', '硒'], 35: ['Br', '溴'],
        36: ['Kr', '氪'], 37: ['Rb', '铷'], 38: ['Sr', '锶'], 39: ['Y', '钇'], 40: ['Zr', '锆'],
        41: ['Nb', '铌'], 42: ['Mo', '钼'], 43: ['Tc', '锝'], 44: ['Ru', '钌'], 45: ['Rh', '铑'],
        46: ['Pd', '钯'], 47: ['Ag', '银'], 48: ['Cd', '镉'], 49: ['In', '铟'], 50: ['Sn', '锡'],
        51: ['Sb', '锑'], 52: ['Te', '碲'], 53: ['I', '碘'], 54: ['Xe', '氙'], 55: ['Cs', '铯'],
        56: ['Ba', '钡'], 57: ['La', '镧'], 58: ['Ce', '铈'], 59: ['Pr', '镨'], 60: ['Nd', '钕'],
        61: ['Pm', '钷'], 62: ['Sm', '钐'], 63: ['Eu', '铕'], 64: ['Gd', '钆'], 65: ['Tb', '铽'],
        66: ['Dy', '镝'], 67: ['Ho', '钬'], 68: ['Er', '铒'], 69: ['Tm', '铥'], 70: ['Yb', '镱'],
        71: ['Lu', '镥'], 72: ['Hf', '铪'], 73: ['Ta', '钽'], 74: ['W', '钨'], 75: ['Re', '铼'],
        76: ['Os', '锇'], 77: ['Ir', '铱'], 78: ['Pt', '铂'], 79: ['Au', '金'], 80: ['Hg', '汞'],
        81: ['Tl', '铊'], 82: ['Pb', '铅'], 83: ['Bi', '铋'], 84: ['Po', '钋'], 85: ['At', '砹'],
        86: ['Rn', '氡'], 87: ['Fr', '钫'], 88: ['Ra', '镭'], 89: ['Ac', '锕'], 90: ['Th', '钍'],
        91: ['Pa', '镤'], 92: ['U', '铀'], 93: ['Np', '镎'], 94: ['Pu', '钚'], 95: ['Am', '镅'],
        96: ['Cm', '锔'], 97: ['Bk', '锫'], 98: ['Cf', '锎'], 99: ['Es', '锿'], 100: ['Fm', '镄']}
# 支壳层排布顺序（按照能级能量排序）
SUBSHELL_SEQUENCE = ['1s',
                     '2s', '2p',
                     '3s', '3p',
                     '3d', '4s', '4p',
                     '4d', '5s', '5p',
                     '4f', '5d', '6s',
                     '6p',
                     '5f', '7s', '7p']
# 支壳层排布顺序（按照名称排序）
SUBSHELL_NAME = ['1s',
                 '2s', '2p',
                 '3s', '3p', '3d',
                 '4s', '4p', '4d', '4f',
                 '5s', '5p', '5d', '5f', '5g',
                 '6s', '6p', '6d', '6f', '6g', '6h',
                 '7s', '7p', '7d', '7f', '7g', '7h', '7i']
# 角量子数名称
ANGULAR_QUANTUM_NUM_NAME = ['s', 'p', 'd', 'f', 'g', 'h', 'i']
_path_ = Path(__file__)
ATOM_INFO = json.load(open(_path_.parent / 'IonsInfo.json', 'r'))

# 电离能
IONIZATION_ENERGY = {}
for key_, value_ in ATOM_INFO['energy'].items():
    temp_dict = {}
    for key__, value__ in value_.items():
        temp_dict[int(key__)] = value__
    IONIZATION_ENERGY[int(key_)] = temp_dict

# 旧的电离能
OLD_IONIZATION_ENERGY = {}
for key_, value_ in ATOM_INFO['old_energy'].items():
    temp_dict = {}
    for key__, value__ in value_.items():
        temp_dict[int(key__)] = value__
    OLD_IONIZATION_ENERGY[int(key_)] = temp_dict

# 基组态
BASE_CONFIGURATION = {}
for num_, config in ATOM_INFO['config'].items():
    temp_dict = {}
    for key_, value_ in config.items():
        temp_dict[int(key_)] = value_
    BASE_CONFIGURATION[int(num_)] = temp_dict

# 最外层电子数
OUTER_ELECTRON_NUM = {}
for num_, electron_num in ATOM_INFO['outermost_electron_num'].items():
    temp_dict = {}
    for key_, value_ in electron_num.items():
        temp_dict[int(key_)] = value_
    OUTER_ELECTRON_NUM[int(num_)] = temp_dict
