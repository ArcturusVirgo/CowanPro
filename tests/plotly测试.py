import plotly.graph_objects as go

from plotly.offline import plot

exp_points_x = [1, 2, 3, 4, 5]
exp_points_y = [1, 2, 3, 4, 5]
cal_points_x = [1, 2, 3, 4, 5]
cal_points_y = [1, 2, 1, 4, 5]

trace1 = go.Scatter(
    x=exp_points_x, y=exp_points_y, mode='lines', line={'color': 'rgb(98, 115, 244)'}
)
trace2 = go.Scatter(
    x=cal_points_x, y=cal_points_y, mode='lines', line={'color': 'rgb(237, 78, 64)'}
)
data = [trace1, trace2]
layout = go.Layout(
    margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
    # xaxis=go.layout.XAxis(range=self.exp_data.x_range),
)
# yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
fig = go.Figure(data=data, layout=layout)
plot(fig, filename=r'F:\Project\Python\PyCharm\CowanPro\tests\aaa.html', auto_open=True)
