def cal_abundance(self):
    """
    获取离子丰度

    """

    def calculate_a_over_S(a_ratios):
        """
        已知a1/a2, a2/a3, ..., a_n-1/a_n，计算a1/S, a2/S, ..., a_n/S，其中S=a1+a2+...+a_n

        Args:
            a_ratios: a1/a2, a2/a3, ..., a_n-1/a_n

        Returns:
            a1/S, a2/S, ..., a_n/S
        """
        a = np.zeros(len(a_ratios) + 1)
        a[0] = 1
        for i in range(1, len(a)):
            a[i] = a[i - 1] * a_ratios[i - 1]

        # 计算S
        S_ = np.sum(a)

        # 计算a1/S, a2/S, ..., a_n/S
        a_over_S = a / S_

        return a_over_S

    cowan_element = {}
    # 按元素分类
    for cowan in self.cowan_list:
        cowan_element[cowan.in36.atom.symbol] = cowan_element.get(cowan.in36.atom.symbol, []) + [cowan]

    abundance_element = {}
    # 计算每个元素的丰度
    for element, cowan_list in cowan_element.items():
        temperature = self.temperature
        electron_density = self.electron_density

        atom_nums = cowan_list[0].in36.atom.num
        ion_num = np.array([k for k in range(atom_nums)])
        ion_energy = np.array([OLD_IONIZATION_ENERGY[atom_nums][k] for k in range(atom_nums)])
        electron_num = np.array([OUTER_ELECTRON_NUM[atom_nums][k] for k in range(atom_nums)])

        S = (9 * 1e-6 * electron_num * np.sqrt(temperature / ion_energy) * np.exp(-ion_energy / temperature)) / (
                ion_energy ** 1.5 * (4.88 + temperature / ion_energy))
        Ar = (5.2 * 1e-14 * np.sqrt(ion_energy / temperature) * ion_num * (
                0.429 + 0.5 * np.log(ion_energy / temperature) + 0.469 * np.sqrt(temperature / ion_energy)))
        A3r = (2.97 * 1e-27 * electron_num / (temperature * ion_energy ** 2 * (4.88 + temperature / ion_energy)))
        ratio = S / (Ar + electron_density * A3r)
        abundance = calculate_a_over_S(ratio)

        abundance_element[element] = abundance

    self.abundance = abundance_element