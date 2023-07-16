from pathlib import Path
from pprint import pprint
from typing import List, Union

from atom import *

class In36:
    def __init__(self):
        self.control_card: List[str] = []
        self.configuration_card: List[Union[list[str], int]] = []

        self.__atomic_num = -1  # 原子序数
        self.__atomic_ion = -1  # 离化度（失去的电子数目）

    def read_from_file(self, path: Path):
        """
        读取in36文件
        Args:
            path (Path): in36文件的路径
        """
        with open(path, 'r') as f:
            lines = f.readlines()
        # 控制卡读入
        control_card_text = lines[0]
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
            v0 = '{:>5}'.format(value[0])
            v1 = '{:>9}'.format(value[1])
            v2 = '{:>7}'.format(value[2])
            v3 = '             '
            v4 = ' '.join(value[3:])
            input_card_list.append([[v0, v1, v2, v3, v4], self.__judge_parity(v4)])
        self.control_card, self.configuration_card = control_card_list, input_card_list

    def add_configuration(self, configuration: str):
        """
        添加组态（会自动剔除重复数据）
        Args:
            configuration(str): 要添加的组态
        """
        if self.configuration_card:  # 如果组态卡不为空
            temp_list = list(zip(*self.configuration_card))[-1]
        else:  # 如果组态卡为空
            temp_list = []
        if configuration not in temp_list:
            v0 = '{:>5}'.format(self.__atomic_num)
            v1 = '{:>9}'.format(f'{self.__atomic_ion + 1}{ATOM[self.__atomic_num][0]}+{self.__atomic_ion}')
            v2 = '{:>7}'.format('11111')
            v3 = '             '
            v4 = configuration
            self.configuration_card.append([[v0, v1, v2, v3, v4], self.__judge_parity(v4)])

    def configuration_move(self, index, opt: str):
        if opt == 'up':
            if 1 <= index <= len(self.configuration_card):
                self.configuration_card[index], self.configuration_card[index - 1] \
                    = self.configuration_card[index - 1], self.configuration_card[index]
        elif opt == 'down':
            if 0 <= index <= len(self.configuration_card) - 2:
                self.configuration_card[index], self.configuration_card[index + 1] \
                    = self.configuration_card[index + 1], self.configuration_card[index]
        else:
            raise ValueError('opt must be "up" or "down"')

    def del_configuration(self, index):
        self.configuration_card.pop(index)

    def get_in36_text(self):
        in36 = ''
        in36 += ''.join(self.control_card)
        in36 += '\n'
        for v in self.configuration_card:
            in36 += ''.join(v)
            in36 += '\n'
        in36 += '   -1\n'
        return in36

    def save_as_in36(self, path: Path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.get_in36_text())

    @staticmethod
    def __judge_parity(configuration: str) -> int:
        """
        判断指定组态的宇称
            Args:
                configuration: 要判断的电子组态

            Returns:
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


class In2:
    def __init__(self):
        self.input_card: List[str] = []

    def read_from_file(self, path):
        with open(path, "r") as f:
            line = f.readline()
        line = line.strip('\n')
        if len(line) != 80:
            line += ' ' * (80 - len(line) - 1)
        rules = [5, 2, 1, 2, 1, 2, 7, 1, 8, 8, 8, 4, 1, 2, 2, 2, 2, 2, 5, 5, 1, 1, 1, 1, 1, 5]
        input_card_list = []
        for rule in rules:
            input_card_list.append(line[:rule])
            line = line[rule:]
        self.input_card = input_card_list

    def get_in2_text(self):
        in2 = ''
        in2 += ''.join(self.input_card)
        in2 += '\n'
        in2 += '        -1\n'
        return in2

    def save_as_in2(self, path: Path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.get_in2_text())


class Cowan:
    pass



if __name__ == '__main__':
    in36 = In36()
    in36.read_from_file(Path('../temp_file/in36'))
    pprint(in36.configuration_card)
