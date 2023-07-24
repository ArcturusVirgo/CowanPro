from pathlib import Path

from cowan import PROJECT_PATH
from cowan.cowan import In36, Atom, In2, ExpData, Cowan, SimulateSpectral

in36_3 = In36(Atom(1, 0))
in36_3.read_from_file(PROJECT_PATH / 'in36_3')
in36_4 = In36(Atom(1, 0))
in36_4.read_from_file(PROJECT_PATH / 'in36_4')
in36_5 = In36(Atom(1, 0))
in36_5.read_from_file(PROJECT_PATH / 'in36_5')
in36_6 = In36(Atom(1, 0))
in36_6.read_from_file(PROJECT_PATH / 'in36_6')

in2 = In2()
in2.read_from_file(PROJECT_PATH / 'in2')

exp_data = ExpData(PROJECT_PATH / 'exp_data.csv')

cowan_3 = Cowan(in36_3, in2, 'Al_3', exp_data)
cowan_4 = Cowan(in36_4, in2, 'Al_4', exp_data)
cowan_5 = Cowan(in36_5, in2, 'Al_5', exp_data)
cowan_6 = Cowan(in36_6, in2, 'Al_6', exp_data)

sim = SimulateSpectral()
sim.add_cowan(cowan_3, cowan_4, cowan_5, cowan_6)
for c in sim.cowan_list:
    c.run()
    c.cal_data.widen_all.widen(23.5)
sim.load_exp_data(Path('f:/Cowan/Al/exp_data.csv'))
sim.get_simulate_data(23.5, 1e20)
print(sim.spectrum_similarity)