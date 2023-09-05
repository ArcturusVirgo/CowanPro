# ================================================
# 本文件用来存储与原子的信息
# ================================================

# 原子信息
ATOM = {1: ['H', '氢'], 2: ['He', '氦'], 3: ['Li', '锂'], 4: ['Be', '铍'], 5: ['B', '硼'],
        6: ['C', '碳'], 7: ['N', '氮'], 8: ['O', '氧'], 9: ['F', '氟'], 10: ['Ne', '氖'],
        11: ['Na', '钠'], 12: ['Mg', '镁'], 13: ['Al', '铝'], 14: ['Si', '硅'], 15: ['Pi', '磷'],
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
# 电离能
IONIZATION_ENERGY = {
    13: [5.985769, 18.82855, 28.447642, 119.9924, 153.8252, 190.49, 241.76, 284.64, 330.21, 398.65, 442.005, 2085.97702,
         2304.140359],
    32: [0.6504E+01, 0.1458E+02, 0.3371E+02, 0.4491E+02, 0.8851E+02, 0.1158E+03, 0.1453E+03, 0.1768E+03, 0.2102E+03,
         0.2455E+03, 0.2835E+03, 0.3223E+03, 0.3629E+03, 0.4050E+03, 0.5257E+03, 0.5669E+03, 0.6088E+03, 0.6515E+03,
         0.7020E+03, 0.7463E+03, 0.8360E+03, 0.8771E+03, 0.2176E+04, 0.2303E+04, 0.2433E+04, 0.2565E+04, 0.2738E+04,
         0.2875E+04, 0.3072E+04, 0.3180E+04, 0.1349E+05, 0.1412E+05]
}

# 基组态
Ne = '1s02 2s02 2p06 '
Ar = Ne + '3s02 3p06 '
Kr = Ar + '3d10 4s02 4p06 '
Xe = Kr + '4d10 5s02 5p06 '
Hg = Xe + '4f14 5d10 6s02 '
Rn = Hg + '6p06 '
BASE_CONFIGURATION = {
    1: '1s01',
    2: '1s02',
    3: '1s02 2s01',
    4: '1s02 2s02',
    5: '1s02 2s02 2p01',
    6: '1s02 2s02 2p02',
    7: '1s02 2s02 2p03',
    8: '1s02 2s02 2p04',
    9: '1s02 2s02 2p05',
    10: '1s02 2s02 2p06',
    11: Ne + '3s01',
    12: Ne + '3s02',
    13: Ne + '3s02 3p01',
    14: Ne + '3s02 3p02',
    15: Ne + '3s02 3p03',
    16: Ne + '3s02 3p04',
    17: Ne + '3s02 3p05',
    18: Ne + '3s02 3p06',
    19: Ar + '4s01',
    20: Ar + '4s02',
    21: Ar + '3d01 4s02',
    22: Ar + '3d02 4s02',
    23: Ar + '3d03 4s02',
    24: Ar + '3d05 4s01',
    25: Ar + '3d05 4s02',
    26: Ar + '3d06 4s02',
    27: Ar + '3d07 4s02',
    28: Ar + '3d08 4s02',
    29: Ar + '3d10 4s01',
    30: Ar + '3d10 4s02',
    31: Ar + '3d10 4s02 4p01',
    32: Ar + '3d10 4s02 4p02',
    33: Ar + '3d10 4s02 4p03',
    34: Ar + '3d10 4s02 4p04',
    35: Ar + '3d10 4s02 4p05',
    36: Ar + '3d10 4s02 4p06',
    37: Kr + '5s01',
    38: Kr + '5s02',
    39: Kr + '4d01 5s02',
    40: Kr + '4d02 5s02',
    41: Kr + '4d04 5s01',
    42: Kr + '4d05 5s01',
    43: Kr + '4d05 5s02',
    44: Kr + '4d07 5s01',
    45: Kr + '4d08 5s01',
    46: Kr + '4d10',
    47: Kr + '4d10 5s01',
    48: Kr + '4d10 5s02',
    49: Kr + '4d10 5s02 5p01',
    50: Kr + '4d10 5s02 5p02',
    51: Kr + '4d10 5s02 5p03',
    52: Kr + '4d10 5s02 5p04',
    53: Kr + '4d10 5s02 5p05',
    54: Kr + '4d10 5s02 5p06',
    55: Xe + '6s01',
    56: Xe + '6s02',
    57: Xe + '5d01 6s02',
    58: Xe + '4f01 5d01 6s02',
    59: Xe + '4f03 6s02',
    60: Xe + '4f04 6s02',
    61: Xe + '4f05 6s02',
    62: Xe + '4f06 6s02',
    63: Xe + '4f07 6s02',
    64: Xe + '4f07 5d01 6s02',
    65: Xe + '4f09 6s02',
    66: Xe + '4f10 6s02',
    67: Xe + '4f11 6s02',
    68: Xe + '4f12 6s02',
    69: Xe + '4f13 6s02',
    70: Xe + '4f14 6s02',
    71: Xe + '4f14 5d01 6s02',
    72: Xe + '4f14 5d02 6s02',
    73: Xe + '4f14 5d03 6s02',
    74: Xe + '4f14 5d04 6s02',
    75: Xe + '4f14 5d05 6s02',
    76: Xe + '4f14 5d06 6s02',
    77: Xe + '4f14 5d07 6s02',
    78: Xe + '4f14 5d09 6s01',
    79: Xe + '4f14 5d10 6s01',
    80: Xe + '4f14 5d10 6s02',
    81: Hg + '6p01',
    82: Hg + '6p02',
    83: Hg + '6p03',
    84: Hg + '6p04',
    85: Hg + '6p05',
    86: Hg + '6p06',
    87: Rn + '7s01',
    88: Rn + '7s02',
    89: Rn + '6d01 7s02',
    90: Rn + '6d02 7s02',
    91: Rn + '5f02 6d01 7s02',
    92: Rn + '5f03 6d01 7s02',
    93: Rn + '5f04 6d01 7s02',
    94: Rn + '5f06 7s02',
    95: Rn + '5f07 7s02',
    96: Rn + '5f07 6d01 7s02',
    97: Rn + '5f09 7s02',
    98: Rn + '5f10 7s02',
    99: Rn + '5f11 7s02',
    100: Rn + '5f12 7s02',
}
