from .AtomInfo import (
    ATOM,
    SUBSHELL_NAME,
    SUBSHELL_SEQUENCE,
    BASE_CONFIGURATION,
    ANGULAR_QUANTUM_NUM_NAME,
)


class Atom:
    def __init__(self, num: int, ion: int):
        """
        原子类，附属于 in36 对象

        Args:
            num: 原子序数
            ion: 离化度（剥离的电子数目）

        Notes:
            1. 使用 get_base_configuration 获取基组态
            2. 使用 arouse_electron 激发电子
            3. 使用 get_configuration 获取当前的电子组态
            4. 使用 revert_to_ground_state 将原子状态重置为基态
            5. goto 2

        """
        self.num = num  # 原子序数
        self.symbol = ATOM[self.num][0]  # 元素符号
        self.name = ATOM[self.num][1]  # 元素名称
        self.ion = ion  # 离化度
        self.electron_num = self.num - self.ion  # 实际的电子数量
        self.electron_arrangement = self.get_base_electron_arrangement()
        self.base_configuration = self.get_base_configuration()  # 基组态

    def get_base_electron_arrangement(self):
        """
        获取原子处于基态时，核外电子的排布情况

        Returns:
            返回一个字典，键为子壳层，值为子壳层的电子数, 例如 {
                '1s': 2,
                '2s': 2,
                '2p': 6,
                '3s': 2,
                '3p': 4,}

        """
        electron_arrangement = {}
        for key, value in map(lambda x: [str(x[:2]), int(x[2:])], BASE_CONFIGURATION[self.num][self.ion].split(' ')):
            electron_arrangement[key] = value
        return electron_arrangement

    def get_base_configuration(self):
        """
        将电子组态重置为基态，并且 获取基组态字符串

        """
        self.revert_to_ground_state()
        return self.get_configuration()

    def get_configuration(self) -> str:
        """
        根据该原子当前的电子排布情况，获取当前的电子组态

        Returns:
            返回一个字符串，例如 3s02 3p03 4s01
        """
        configuration = {}  # 按照子壳层的顺序排列的电子组态
        for i, subshell_name in enumerate(SUBSHELL_NAME):
            if subshell_name in self.electron_arrangement.keys():
                configuration[subshell_name] = self.electron_arrangement[subshell_name]
        delete_name = []
        for i, (subshell_name, num) in enumerate(configuration.items()):
            l_ = ANGULAR_QUANTUM_NUM_NAME.index(subshell_name[1])
            if num == 4 * l_ + 2:
                delete_name.append(subshell_name)
            else:
                delete_name.append(subshell_name)
                break
        if len(delete_name) >= 2:
            delete_name.pop(-1)
            delete_name.pop(-1)
        else:
            delete_name = []
        for name in delete_name:
            configuration.pop(name)

        configuration_list = []
        for name, num in configuration.items():
            configuration_list.append('{}{:0>2}'.format(name, num))
        return ' '.join(configuration_list)

    def arouse_electron(self, low_name, high_name):
        """
        激发电子，改变原子内电子的排布情况

        Args:
            low_name: 下态的支壳层名称
            high_name: 上态的支壳层名称
        """
        if low_name not in SUBSHELL_SEQUENCE:
            raise Exception(f'没有名为{low_name}的支壳层！')
        elif high_name not in SUBSHELL_SEQUENCE:
            raise Exception(f'没有名为{high_name}的支壳层!')
        elif low_name not in self.electron_arrangement.keys():
            raise Exception(f'没有处于{low_name}的电子！')
        elif self.electron_arrangement.get(high_name, 0) == 4 * ANGULAR_QUANTUM_NUM_NAME.index(high_name[1]) + 2:
            raise Exception(f'{high_name}的电子已经排满！')

        self.electron_arrangement[low_name] -= 1
        self.electron_arrangement[high_name] = (self.electron_arrangement.get(high_name, 0) + 1)
        if self.electron_arrangement[low_name] == 0:
            self.electron_arrangement.pop(low_name)

    def revert_to_ground_state(self):
        """
        将原子的状态重置为基态

        """
        self.electron_arrangement = self.get_base_electron_arrangement()

    def load_class(self, class_info):
        self.num = class_info.num
        self.symbol = class_info.symbol
        self.name = class_info.name
        self.ion = class_info.ion
        self.electron_num = class_info.electron_num
        self.electron_arrangement = class_info.electron_arrangement
        self.base_configuration = class_info.base_configuration
