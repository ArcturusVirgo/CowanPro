import copy
from typing import Optional, List
from pathlib import Path
from itertools import groupby

from .Atom import Atom
from .AtomInfo import ATOM, ANGULAR_QUANTUM_NUM_NAME


class In36:
    def __init__(self):
        """
        in36 对象，一般附属于 Cowan 对象

        """
        self.atom: Optional[Atom] = None

        self.control_card = ['2', ' ', ' ', '-9', ' ', '  ', ' 2', '   ', '10', '  1.0', '    5.e-08', '    1.e-11',
                             '-2', '  ', ' ', '1', '90', '  ', '  1.0', ' 0.65', '  0.0', '  0.0', '     ', ]
        self.configuration_card = []

    def read_from_file(self, path: Path):
        """
        读取已经编写号的in36文件

        自动更新原子对象，组态卡，控制卡

        Args:
            path (Path): in36文件的路径
        """
        with open(path, 'r') as f:
            lines = f.readlines()
        # 控制卡读入
        control_card_text = lines[0].strip('\n')
        control_card_list = []
        if len(control_card_text) != 80:
            control_card_text += ' ' * (80 - len(control_card_text))
        rules = [1, 1, 1, 2, 1, 2, 2, 3, 2, 5, 10, 10, 2, 2, 1, 1, 2, 2, 5, 5, 5, 5, 5]
        for rule in rules:
            control_card_list.append(control_card_text[:rule])
            control_card_text = control_card_text[rule:]
        # 组态卡读入
        input_card_list = []
        for line in lines[1:]:
            value = line.split()
            if value == ['-1']:
                break
            atom_num = line[1:5]
            ion = line[8:10]
            label = line[10:28]
            con = line[32:].strip(' ')
            input_card_list.append([[atom_num, ion, label, con], self.__judge_parity(con)])
        self.control_card, self.configuration_card = control_card_list, input_card_list

        # 更新原子信息
        num = int(self.configuration_card[0][0][0])
        ion = int(self.configuration_card[0][0][1]) - 1
        self.atom = Atom(num=num, ion=ion)

    def set_atom(self, atom: Atom):
        """
        设置原子对象

        Args:
            atom (Atom): 原子对象

        """
        self.atom = copy.deepcopy(atom)

    def set_control_card(self, control_card: List[str]):
        """
        设置控制卡

        Args:
            control_card: 控制卡列表

        """
        self.control_card = copy.deepcopy(control_card)

    def add_configuration(self, configuration: str):
        """
        向 in36 文件的组态卡添加组态（会自动剔除重复的组态）

        Args:
            configuration (str): 要添加的组态
        """
        if self.configuration_card:  # 如果组态卡不为空
            temp_list = list(zip(*list(zip(*self.configuration_card))[0]))[-1]
        else:  # 如果组态卡为空
            temp_list = []
        if configuration not in temp_list:
            v0 = f'{self.atom.num}'
            v1 = f'{self.atom.ion + 1}'
            v2 = f'{ATOM[self.atom.num][0]}+{self.atom.ion}'
            v3 = configuration
            self.configuration_card.append([[v0, v1, v2, v3], self.__judge_parity(v3)])

    def configuration_move(self, index, opt: str):
        """
        移动组态的先后顺序

        Args:
            index: 要移动的组态的索引
            opt: 操作名称 up 或 down

        """
        if opt == 'up':
            if 1 <= index <= len(self.configuration_card):
                self.configuration_card[index], self.configuration_card[index - 1] = (
                    self.configuration_card[index - 1], self.configuration_card[index],)
        elif opt == 'down':
            if 0 <= index <= len(self.configuration_card) - 2:
                self.configuration_card[index], self.configuration_card[index + 1] = (
                    self.configuration_card[index + 1], self.configuration_card[index],)
        else:
            raise ValueError('opt must be "up" or "down"')

    def del_configuration(self, index: int):
        """
        删除 in36 组态卡中的组态

        Args:
            index (int): 要删除的组态的索引

        """
        self.configuration_card.pop(index)

    def get_configuration_name(self, low_index, high_index):
        """
        根据组态索引获取电子跃迁的支壳层名称

        Args:
            low_index: 下态的索引
            high_index: 上态的索引

        Returns:
            返回一个字符串，如 '2p --> 3s'
        """
        first_parity = self.configuration_card[0][1]
        first_configuration = []
        second_configuration = []
        for configuration, parity in self.configuration_card:
            if parity == first_parity:
                first_configuration.append(configuration[-1])
            else:
                second_configuration.append(configuration[-1])
        low_index_, high_index_ = low_index - 1, high_index - 1
        low_configuration = first_configuration[low_index_]
        high_configuration = second_configuration[high_index_]

        low_configuration = low_configuration.split(' ')
        high_configuration = high_configuration.split(' ')

        low_dict = {}
        high_dict = {}

        for low in low_configuration:
            low_dict[low[:2]] = low[2:]
        for high in high_configuration:
            high_dict[high[:2]] = high[2:]
        configuration_name = list(set(list(low_dict.keys()) + list(high_dict.keys())))
        res = {}
        for name in configuration_name:
            res[name] = int(low_dict.get(name, 0)) - int(high_dict.get(name, 0))
        low_name = []
        high_name = []
        for key, value in res.items():
            if value < 0:
                for i in range(-value):
                    high_name.append(key)
            elif value > 0:
                for i in range(value):
                    low_name.append(key)
        return '{} --> {}'.format(','.join(low_name), ','.join(high_name))

    def get_text(self):
        """
        生成 in36 文件所包含的字符串

        Returns:
            in36 文件的字符串
        """
        # 控制卡
        in36 = ''
        in36 += ''.join(self.control_card)
        in36 += '\n'
        # 组态卡
        for v in self.configuration_card:
            in36 += ' '
            in36 += '{:>4}'.format(v[0][0])
            in36 += ' ' * 3
            in36 += '{:>2}'.format(v[0][1])
            in36 += '{:<18}'.format(v[0][2])
            in36 += ' ' * 4
            in36 += v[0][3]
            in36 += '\n'
        in36 += '   -1\n'
        return in36

    def get_atom_info(self) -> (int, int, str):
        """
        获取原子的基本信息
        Returns: (num, ion, symbol)
            Examples: (1, 0, 'H')
        """
        return self.atom.get_atom_info()

    def save(self, path: Path):
        """
        保存为 in36 文件

        Args:
            path (Path): 生成的 in36 文件的路径

        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.get_text())

    @staticmethod
    def __judge_parity(configuration: str) -> int:
        """
        判断指定组态的宇称

        Args:
            configuration: 要判断宇称的电子组态，字符串形式，如 '2p06 3s01'

        Returns:
            返回一个整数，其中
            0: 偶宇称
            1: 奇宇称
        """
        configuration = list(configuration.split(' '))
        sum_ = 0
        for v in configuration:
            sum_ += ANGULAR_QUANTUM_NUM_NAME.index(v[1]) * eval(v[3:])

        if sum_ % 2 == 0:
            return 0
        else:
            return 1

    def load_class(self, class_info):
        # atom 对象
        self.atom.load_class(class_info.atom)
        self.control_card = class_info.control_card
        # self.configuration_card = class_info.configuration_card
        # # 更新in36输入文件
        temp_configuration_card = []
        # # 新的组态卡
        # # [原子序数，离化度+1，标记，组态]
        for configuration_card, parity in class_info.configuration_card:
            atom_num = configuration_card[0].strip(' ')
            ion_with_symbol = configuration_card[1].strip(' ')
            configuration = configuration_card[4].strip(' ')
            info_list = [''.join(list(g)) for k, g in groupby(ion_with_symbol, key=lambda x: x.isdigit())]
            ion_add_1 = info_list[0]
            label = ''.join(info_list[1:])
            temp_configuration_card.append([[atom_num, ion_add_1, label, configuration], parity])
        self.configuration_card = temp_configuration_card


class In2:
    def __init__(self):
        """
        in2 对象，附属于 Cowan 对象

        Args:

        """
        self.input_card: List[str] = [
            'g5inp', '  ', '0', ' 0', '0', '00', '  0.000', ' ', '00000000', ' 0000000', '   00000', ' 000', '0', '90',
            '99', '90', '90', '90', '.0000', '     ', '0', '7', '2', '2', '9', '     ', ]
        self.index_rule = [
            [1 - 1, 5],
            [6 - 1, 7],
            [8 - 1, 8],
            [9 - 1, 10],
            [11 - 1, 11],
            [12 - 1, 13],
            [14 - 1, 20],
            [21 - 1, 21],
            [22 - 1, 29],  # 22-49
            [30 - 1, 37],  # 22-49
            [38 - 1, 45],  # 22-49
            [46 - 1, 49],  # 22-49
            [50 - 1, 50],
            [51 - 1, 52],  # 51-60
            [53 - 1, 54],  # 51-60
            [55 - 1, 56],  # 51-60
            [57 - 1, 58],  # 51-60
            [59 - 1, 60],  # 51-60
            [61 - 1, 65],
            [66 - 1, 70],
            [71 - 1, 71],
            [72 - 1, 72],
            [73 - 1, 73],
            [74 - 1, 74],
            [75 - 1, 75],
            [76 - 1, 80],
        ]
        self.rule = [5, 2, 1, 2, 1, 2, 7, 1, 8, 8, 8, 4, 1, 2, 2, 2, 2, 2, 5, 5, 1, 1, 1, 1, 1, 5, ]

    def read_from_file(self, path: Path):
        """
        读取 in2 文件

        更新输入卡

        Args:
            path: in2文件的路径

        """
        with open(path, 'r') as f:
            line = f.readline()
        line = line.strip('\n')
        if len(line) != 80:
            line += ' ' * (80 - len(line) - 1)
        input_card_list = []
        for rule in self.rule:
            input_card_list.append(line[:rule])
            line = line[rule:]
        self.input_card = input_card_list

    def set_in2_list(self, in2_list: List[str]):
        """
        设置输入卡

        Args:
            in2_list: 输入卡列表

        """
        self.input_card = copy.deepcopy(in2_list)

    def get_text(self):
        """
        获取 in2 文件所包含的字符串

        Returns:
            in2 字符串
        """

        in2 = 'g5inp     000 0.0000          01        .095.095  8499848484 0.00   1 18229'
        new_in2 = (
                in2[:5] +
                f'{self.input_card[1][:self.rule[1]]}'  # RCK 用于调整输出
                + in2[7:50] +
                ''.join(self.input_card[13:18]) +  # salter 因子
                in2[60:]
        )
        new_in2 += '\n'
        new_in2 += '        -1\n'
        return new_in2

    def save(self, path: Path):
        """
        保存为 in2 文件

        Args:
            path: 要保存的文件夹

        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.get_text())

    def load_class(self, class_info):
        self.input_card = class_info.input_card
        # start [1.0.2 > 1.0.3]
        if hasattr(class_info, 'rule'):
            self.rule = class_info.rule
        else:
            self.rule = [5, 2, 1, 2, 1, 2, 7, 1, 8, 8, 8, 4, 1, 2, 2, 2, 2, 2, 5, 5, 1, 1, 1, 1, 1, 5, ]
        if hasattr(class_info, 'index_rule'):
            self.index_rule = class_info.index_rule
        else:
            self.index_rule = [
                [1 - 1, 5],
                [6 - 1, 7],
                [8 - 1, 8],
                [9 - 1, 10],
                [11 - 1, 11],
                [12 - 1, 13],
                [14 - 1, 20],
                [21 - 1, 21],
                [22 - 1, 29],  # 22-49
                [30 - 1, 37],  # 22-49
                [38 - 1, 45],  # 22-49
                [46 - 1, 49],  # 22-49
                [50 - 1, 50],
                [51 - 1, 52],  # 51-60
                [53 - 1, 54],  # 51-60
                [55 - 1, 56],  # 51-60
                [57 - 1, 58],  # 51-60
                [59 - 1, 60],  # 51-60
                [61 - 1, 65],
                [66 - 1, 70],
                [71 - 1, 71],
                [72 - 1, 72],
                [73 - 1, 73],
                [74 - 1, 74],
                [75 - 1, 75],
                [76 - 1, 80],
            ]
        # end [1.0.2 > 1.0.3]
