import copy
from typing import List, Dict

from .Cowan_ import Cowan
from .ExpData import ExpData


class CowanList:
    def __init__(self):
        """
        用于存储 cowan 对象
        """
        self.chose_cowan: List[str] = []  # 用于存储 cowan 对象在历史列表中的索引
        self.add_or_not: List[bool] = []  # cowan 对象是否被添加

        self.cowan_run_history: Dict[str:Cowan] = {}  # 用于存储 cowan 对象

    def sort_chose_cowan(self):
        self.chose_cowan = sorted(self.chose_cowan, key=lambda x: (x.split('_')[0], int(x.split('_')[1])))

    def add_cowan(self, key):
        """
        从历史记录中 添加 cowan 对象，如果列表中已经存在就删除再添加

        Args:
            key: 要添加的 cowan 对象的名称（name属性）

        """
        if key in self.chose_cowan:
            self.del_cowan(key)
        self.chose_cowan.append(key)
        self.add_or_not.append(True)

    def del_cowan(self, key):
        """
        删除 cowan 对象

        Args:
            key: 要删除的 cowan 对象的名称（name属性）

        """
        index = self.chose_cowan.index(key)
        self.chose_cowan.pop(index)
        self.add_or_not.pop(index)

    def add_history(self, cowan: Cowan):
        """
        向历史记录中添加 cowan 对象，如果了已经存在，就删除再添加
        如果它存在于已选择的列表中，就就删除再添加

        Args:
            cowan: 要添加的 cowan 对象

        """
        if cowan.name in self.cowan_run_history.keys():
            self.cowan_run_history.pop(cowan.name)
        self.cowan_run_history[cowan.name] = copy.deepcopy(cowan)
        # 如果它存在于已选择的列表中，就更新它
        if cowan.name in self.chose_cowan:
            self.add_cowan(cowan.name)

    def clear_history(self):
        """
        清空历史记录

        如果它存在于已选择的列表中，就不进行删除操作

        """
        keys = list(self.cowan_run_history.keys())
        for key in keys:
            if key not in self.chose_cowan:
                self.cowan_run_history.pop(key)

    def update_exp_data(self, exp_data: ExpData):
        """
        更新所有cowan对象中的exp_data对象

        Args:
            exp_data: 要更新的exp_data对象

        """
        for cowan in self.cowan_run_history.values():
            cowan.exp_data = exp_data

    def set_xrange(self, x_range, num):
        for cowan in self.cowan_run_history.values():
            cowan.set_xrange(x_range, num)

    def reset_xrange(self):
        for cowan in self.cowan_run_history.values():
            cowan.reset_xrange()

    def get_cowan_from_name(self, name):
        return self.cowan_run_history[name]

    def get_cowan_from_index(self, index):
        return self.cowan_run_history[self.chose_cowan[index]]

    def is_multi_elemental(self):
        element_set = set()
        for name in self.chose_cowan:
            element = name.split('_')[0]
            element_set.add(element)
        if len(element_set) > 1:
            return True
        else:
            return False

    def load_class(self, class_info):
        self.chose_cowan = class_info.chose_cowan
        self.add_or_not = class_info.add_or_not
        for (ok, ov), (nk, nv) in zip(self.cowan_run_history.items(), class_info.cowan_run_history.items()):
            ov.load_class(nv)
            self.cowan_run_history[ok] = ov

    def __getitem__(self, index) -> (Cowan, bool):
        return self.cowan_run_history[self.chose_cowan[index]], self.add_or_not[index]
