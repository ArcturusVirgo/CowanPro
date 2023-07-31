import copy
from pprint import pprint

import numpy as np

from cowan import PROJECT_PATH
from cowan.cowan import In36, Atom, In2, ExpData, Cowan, SimulateSpectral, SpaceTimeResolution

atom = None
simulate = SimulateSpectral()
space_time_resolution = SpaceTimeResolution()
delta = {3: 0.05,
         4: -0.04,
         5: 0.0,
         6: 0.05}
exp_data_1 = ExpData(PROJECT_PATH / './exp_data.csv')
for i in range(3, 7):
    atom = Atom(1, 0)
    in36 = In36(atom)
    in36.read_from_file(PROJECT_PATH / f'in36_{i}')
    in2 = In2()
    cowan = Cowan(in36, in2, f'Al_{i}', exp_data_1, 1)
    cowan.run()
    cowan.cal_data.widen_all.delta_lambda = delta[i]
    cowan.cal_data.widen_all.widen(25.6, False)
    simulate.add_cowan(cowan)
simulate.exp_data = copy.deepcopy(exp_data_1)
for x in range(5):
    for time in range(6):
        temp = 20 + np.random.random() * 30
        dishu = np.random.random() * 10
        zhishu = 17 + np.random.random() * 4
        den = dishu * 10 ** zhishu
        simulate.temperature = temp
        simulate.electron_density = den
        space_time_resolution.add_st((str(time), (str(x), '0', '0')), simulate)
#
space_time_resolution.plot_change_by_space_time(1)
