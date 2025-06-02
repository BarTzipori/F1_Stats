import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_multi_driver_replay(telemetry_data, driver_shapes, team_colors):
    fig, ax = plt.subplots()
    artists = {}

    ref_driver = next(iter(telemetry_data.values()))
    ax.plot(ref_driver['X'], ref_driver['Y'], color='lightgray', linewidth=1.5)

    x_min, x_max = ref_driver['X'].min(), ref_driver['X'].max()
    y_min, y_max = ref_driver['Y'].min(), ref_driver['Y'].max()

    x_pad = (x_max - x_min) * 0.08
    y_pad = (y_max - y_min) * 0.08

    ax.set_xlim(x_min - x_pad, x_max + x_pad)
    ax.set_ylim(y_min - y_pad, y_max + y_pad)

    for code, telemetry in telemetry_data.items():
        marker = driver_shapes.get(code, 'o')
        color = team_colors.get(code, 'black')

        point, = ax.plot([], [], marker=marker, color=color, markersize=6, label=code)
        label = ax.text(0, 0, code, color=color, fontsize=8)
        artists[code] = (point, telemetry, label)

    ax.set_title("Replay: Selected Drivers")
    ax.legend()

    max_len = max(len(t) for t in telemetry_data.values())

    def update(i):
        for code, (point, telemetry, label) in artists.items():
            if i < len(telemetry):
                x = telemetry['X'].iloc[i]
                y = telemetry['Y'].iloc[i]
                point.set_data([x], [y])
                label.set_position((x + 1, y + 1))
        return [a[0] for a in artists.values()] + [a[2] for a in artists.values()]

    ani = animation.FuncAnimation(fig, update, frames=max_len, interval=10, blit=True)
    plt.show()