import numpy as np
import matplotlib.pyplot as plt

class PolarSpiralPlotter:
    def __init__(self, a=1.0, b=0.2, theta_max=5 * np.pi, num_points=1000):
        self.a = a
        self.b = b
        self.theta_max = theta_max
        self.num_points = num_points
        self.theta = np.linspace(0, self.theta_max, self.num_points)
        self.rho = self.a * np.exp(self.b * self.theta)
        self.rho_avg = (self.rho + self.a * np.exp(self.b * (self.theta + 2 * np.pi))) / 2
        self.ray_angles_deg = list(range(0, int(np.rad2deg(self.theta_max)), 30))
        self.intersections = self._compute_exact_intersections()

    def _compute_exact_intersections(self):
        intersections = []
        for angle_deg in self.ray_angles_deg:
            theta = np.deg2rad(angle_deg)

            rho_orig = self.a * np.exp(self.b * theta)
            rho_avg = (rho_orig + self.a * np.exp(self.b * (theta + 2 * np.pi))) / 2

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

    def plot(self):
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='polar')
        ax.plot(self.theta, self.rho, label=fr'$\rho = {self.a}e^{{{self.b}\theta}}$', color='blue')
        ax.plot(self.theta, self.rho_avg, label=r'$\rho_{avg}$', color='orange', linestyle='--')

        max_rho = max(self.rho.max(), self.rho_avg.max()) * 1.05
        for deg in self.ray_angles_deg:
            rad = np.deg2rad(deg)
            ax.plot([rad, rad], [0, max_rho], color='gray', linestyle=':', linewidth=1)

        point_artists = []
        for pt in self.intersections:
            color = 'red' if pt['curve'] == 'original' else 'green'
            p, = ax.plot(pt['theta'], pt['rho'], 'o', color=color, markersize=5, picker=5)
            p._meta = pt
            point_artists.append(p)

        ax.set_title("Interactive Polar Plot (Click Points for Info)", va='bottom')
        ax.legend()
        plt.tight_layout()

        annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.8),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def on_pick(event):
            artist = event.artist
            if hasattr(artist, "_meta"):
                pt = artist._meta
                text = (
                    f"[{pt['curve']}] θ={pt['theta_deg']:.0f}°\n"
                    f"ρ={pt['rho']:.3f}\n"
                    f"x={pt['x']:.3f}, y={pt['y']:.3f}"
                )
                annot.xy = (pt['theta'], pt['rho'])
                annot.set_text(text)
                annot.set_visible(True)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("pick_event", on_pick)
        plt.show()
        
    def get_intersections_cartesian(self):
        """
        返回两个列表：
        - avg_curve_points: [(x, y), ...]
        - original_curve_points: [(x, y), ...]
        """
        avg_curve_points = []
        original_curve_points = []

        for pt in self.intersections:
            coord = (pt['x'], pt['y'])
            if pt['curve'] == 'avg':
                avg_curve_points.append(coord)
            else:
                original_curve_points.append(coord)

        return avg_curve_points, original_curve_points

# 示例调用
if __name__ == "__main__":
    a_input = float(input("请输入 a 的值（默认 1.0）: ") or 1.0)
    b_input = float(input("请输入 b 的值（默认 0.2）: ") or 0.2)
    plotter = PolarSpiralPlotter(a=a_input, b=b_input)
    plotter.plot()
