import numpy as np
import matplotlib.pyplot as plt

def compute_exact_intersections(a, b, angle_deg_list):
    intersections = []

    for angle_deg in angle_deg_list:
        theta = np.deg2rad(angle_deg)

        rho_orig = a * np.exp(b * theta)
        rho_avg = (rho_orig + a * np.exp(b * (theta + 2 * np.pi))) / 2

        x_orig = rho_orig * np.cos(theta)
        y_orig = rho_orig * np.sin(theta)

        x_avg = rho_avg * np.cos(theta)
        y_avg = rho_avg * np.sin(theta)

        intersections.append({
            'curve': 'original',
            'theta_deg': angle_deg,
            'theta': theta,
            'rho': rho_orig,
            'x': x_orig,
            'y': y_orig
        })

        intersections.append({
            'curve': 'avg',
            'theta_deg': angle_deg,
            'theta': theta,
            'rho': rho_avg,
            'x': x_avg,
            'y': y_avg
        })

    return intersections

def plot_interactive(a=1.0, b=0.2, theta_max=5 * np.pi, num_points=1000):
    theta = np.linspace(0, theta_max, num_points)
    rho = a * np.exp(b * theta)
    rho_avg = (rho + a * np.exp(b * (theta + 2 * np.pi))) / 2

    ray_angles_deg = list(range(0, int(np.rad2deg(theta_max)), 30))
    intersections = compute_exact_intersections(a, b, ray_angles_deg)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='polar')
    ax.plot(theta, rho, label=fr'$\rho = {a}e^{{{b}\theta}}$', color='blue')
    ax.plot(theta, rho_avg, label=fr'$\rho_{{avg}}$', color='orange', linestyle='--')

    max_rho = max(rho.max(), rho_avg.max()) * 1.05
    for deg in ray_angles_deg:
        rad = np.deg2rad(deg)
        ax.plot([rad, rad], [0, max_rho], color='gray', linestyle=':', linewidth=1)

    # 绘制交点（带 marker 和元信息）
    point_artists = []
    for pt in intersections:
        color = 'red' if pt['curve'] == 'original' else 'green'
        p, = ax.plot(pt['theta'], pt['rho'], 'o', color=color, markersize=5, picker=5)
        p._meta = pt  # 存入自定义属性，点击时可访问
        point_artists.append(p)

    ax.set_title("Interactive Polar Plot (Click Points for Info)", va='bottom')
    ax.legend()
    plt.tight_layout()

    # 添加注释框
    annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.8),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def on_pick(event):
        artist = event.artist
        if hasattr(artist, "_meta"):
            pt = artist._meta
            theta_deg = pt['theta_deg']
            rho = pt['rho']
            x = pt['x']
            y = pt['y']
            text = (
                f"[{pt['curve']}] θ={theta_deg:.0f}°\n"
                f"ρ={rho:.3f}\n"
                f"x={x:.3f}, y={y:.3f}"
            )
            annot.xy = (pt['theta'], pt['rho'])
            annot.set_text(text)
            annot.set_visible(True)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("pick_event", on_pick)

    plt.show()

# 示例调用
if __name__ == "__main__":
    a_input = float(input("请输入 a 的值（默认 1.0）: ") or 1.0)
    b_input = float(input("请输入 b 的值（默认 0.2）: ") or 0.2)
    plot_interactive(a=a_input, b=b_input)
