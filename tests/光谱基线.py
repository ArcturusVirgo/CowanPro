import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# data = np.loadtxt(r'F:\Project\Python\PyCharm\NewCowan\temp_file\Merge0_0001.Raw8.txt', delimiter=';', skiprows=2)
data = np.loadtxt("f:/Cowan/Al/exp_data.csv", delimiter=",", skiprows=0)
# -----数据读取-----#
x = np.array(data[:, 0])  # 波数
y = np.array(data[:, 1])  # 幅值

# -----归一化&平滑-----#
n = 10  # 拟合阶数
y_filter = savgol_filter(y, 21, 5, mode="nearest")  # SG平滑
y_uniform = (y_filter - min(y_filter)) / (max(y_filter) - min(y_filter))  # 归一化

# -----基线校正-----#
p0 = np.polyfit(x, y_uniform, n)  # 多项式拟合，返回多项式系数
y_fit0 = np.polyval(p0, x)  # 计算拟合值
r0 = y_uniform - y_fit0
dev0 = np.sqrt(np.sum((r0 - np.mean(r0)) ** 2) / len(r0))  # 计算残差
y_remove0 = y_uniform[y_uniform <= y_fit0]  # 峰值消除
x_remove0 = x[np.where(y_uniform <= y_fit0)]  # 峰值消除
i = 0
judge = 1
dev = []
while judge:
    p1 = np.polyfit(x_remove0, y_remove0, n)  # 多项式拟合，返回多项式系数
    y_fit1 = np.polyval(p1, x_remove0)  # 计算拟合值
    r1 = y_remove0 - y_fit1
    dev1 = np.sqrt(np.sum((r1 - np.mean(r1)) ** 2) / len(r1))  # 计算残差
    dev.append(dev1)
    if i == 0:
        judge = abs(dev[i] - dev0) / dev[i] > 0.05
    else:
        judge = abs((dev[i] - dev[i - 1]) / dev[i]) > 0.05  # 残差判断条件
    y_remove0[np.where(y_remove0 <= y_fit1)] = y_fit1[
        np.where(y_remove0 <= y_fit1)
    ]  # 光谱重建
    i = i + 1
y_baseline = np.polyval(p1, x)  # 基线
y_baseline_correction = y_uniform - y_baseline  # 基线校正后

# -----显示-----#
plt.figure(1)
plt.plot(
    x, y_uniform, color="black", linewidth=2.0, linestyle="solid", label="Raw_data"
)
plt.plot(x, y_baseline, color="red", linewidth=2.0, linestyle="solid", label="Baseline")
plt.plot(
    x,
    y_baseline_correction,
    color="blue",
    linewidth=2.0,
    linestyle="solid",
    label="After_correction",
)
plt.title("spetrum", fontsize=30)  # 设置图的标题
plt.legend(loc="best")  # 图例放到图中的最佳位置
plt.xlabel("wavenumber(cm^-1)", fontsize=14)  # 设置横轴名称以及字体大小
plt.ylabel("amplitude", fontsize=14)  # 设置纵轴

plt.savefig("a_myplot.jpg", dpi=700)  # 保存图片，矢量图
plt.show()
