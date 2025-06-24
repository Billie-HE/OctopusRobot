import numpy as np

class CoordinateTransformer:
    def __init__(self, origin, x_axis_point):
        """
        初始化变换器：
        origin: 新坐标系原点 (2D)
        x_axis_point: 新坐标系X方向参考点 (2D)
        """
        self.origin = np.array(origin)
        self.x_axis_point = np.array(x_axis_point)
        self.T = self._build_transformation_matrix()

    def _build_transformation_matrix(self):
        """
        构建二维齐次变换矩阵，将世界坐标系变换到以origin为原点、
        以x_axis_point确定X方向的局部坐标系。
        """
        vec_x = self.x_axis_point - self.origin
        vec_x = vec_x / np.linalg.norm(vec_x)

        # Y轴为X轴逆时针旋转90度
        vec_y = np.array([-vec_x[1], vec_x[0]])

        R = np.vstack([vec_x, vec_y]).T  # 2x2旋转矩阵
        t = self.origin.reshape(2, 1)

        T = np.eye(3)
        T[:2, :2] = R.T  # 逆旋转矩阵
        T[:2, 2] = (-R.T @ t).ravel()  # 逆变换的平移部分
        return T

    def transform_points(self, points):
        """
        使用齐次变换矩阵 T 变换 Nx2 点集
        points: numpy数组，形状为 (N, 2)
        返回变换后的点，形状 (N, 2)
        """
        points = np.array(points)
        points_h = np.hstack([points, np.ones((points.shape[0], 1))])  # Nx3
        transformed = (self.T @ points_h.T).T[:, :2]
        return transformed

if __name__ == "__main__":
    print("请输入四个点坐标（x y）：")
    pts = []
    for i in range(4):
        x, y = map(float, input(f"第{i+1}个点: ").split())
        pts.append([x, y])
    points = np.array(pts)

    print("\n请输入新原点坐标（x y）：")
    origin = list(map(float, input().split()))
    print("请输入新X方向参考点坐标（x y）：")
    x_axis_point = list(map(float, input().split()))

    transformer = CoordinateTransformer(origin, x_axis_point)
    new_points = transformer.transform_points(points)

    print("\n=== 变换后坐标（新坐标系下） ===")
    for i, pt in enumerate(new_points):
        print(f"点{i+1}: ({pt[0]:.4f}, {pt[1]:.4f})")
