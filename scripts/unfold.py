from NaturalGrowthCurve import PolarSpiralPlotter
from SimultaneousTransform import CoordinateTransformer
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.cm import get_cmap
from itertools import combinations
myCurves = PolarSpiralPlotter(a=0.5,b=0.2,theta_max=5*np.pi)
avg_data,raw_data = myCurves.get_intersections_cartesian()
section_data = []
for i in range(len(avg_data)-1):
    myTransformer = CoordinateTransformer(origin=avg_data[i],x_axis_point=avg_data[i+1])
    transformed_pts = myTransformer.transform_points(raw_data[i:i+2]+avg_data[i:i+2])
    section_data.append(transformed_pts)
final_data = []
final_data.append(section_data[0])
for i in range(1,len(section_data)):
    volumn = []
    for pt in section_data[i]:
        pt[0] += section_data[i-1][3][0]
        volumn.append(pt)
    final_data.append(volumn)
print(final_data)


cmap = get_cmap("tab20")
for i, points in enumerate(final_data):
    color = cmap(i % 20)
    points = np.array(points)

    # 画所有两两连接线（组合）
    for p1, p2 in combinations(points, 2):  # 共6条边
        x_vals = [p1[0], p2[0]]
        y_vals = [p1[1], p2[1]]
        plt.plot(x_vals, y_vals, color=color, alpha=0.7)

    # 绘制点
    plt.scatter(points[:, 0], points[:, 1], color=color, s=5, label=f'Group {i+1}')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Visualization of point groups in Cartesian coordinates')
plt.legend(loc='best', fontsize='small', ncol=2)
plt.grid(True)
plt.axis('equal')  # 保持 x,y 比例一致
plt.show()