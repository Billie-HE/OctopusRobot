import numpy as np

def build_transformation_matrix(origin, x_axis_point):
    """
    构建二维齐次变换矩阵：将原坐标系变换到以 origin 为原点、x_axis_point 为 X 方向的局部坐标系中
    """
    # 新 X 方向的单位向量
    vec_x = np.array(x_axis_point) - np.array(origin)
    vec_x = vec_x / np.linalg.norm(vec_x)

    # 新 Y 方向为 X 的逆时针旋转 90 度
    vec_y = np.array([-vec_x[1], vec_x[0]])

    # 构造旋转矩阵和平移向量
    R = np.vstack([vec_x, vec_y]).T  # 2x2
    t = np.array(origin).reshape(2, 1)  # 2x1

    # 齐次变换矩阵（世界 -> 新坐标系）
    T = np.eye(3)
    T[:2, :2] = R.T  # 旋转（转置实现逆旋转）
    T[:2, 2] = (-R.T @ t).ravel()  # 平移（逆变换）
    return T

def transform_points(points, T):
    """
    使用齐次矩阵 T 变换多个点
    """
    points_h = np.hstack([points, np.ones((points.shape[0], 1))])  # Nx3
    transformed = (T @ points_h.T).T[:, :2]  # Nx2
    return transformed

# 示例调用
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

    T = build_transformation_matrix(origin, x_axis_point)
    new_points = transform_points(points, T)

    print("\n=== 变换后坐标（新坐标系下） ===")
    for i, pt in enumerate(new_points):
        print(f"点{i+1}: ({pt[0]:.4f}, {pt[1]:.4f})")
