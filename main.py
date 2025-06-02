from utils.telemetry_loader import load_driver_lap
from utils.replay_plotter import run_multi_driver_replay

MARKERS = ['o', 's', '^', 'D', 'P', '*', 'X', 'v', '<', '>']

def main():
    session_year = 2023
    gp_name = 'Monza'
    session_type = 'R'

    print("Enter driver codes (e.g. VER,HAM,LEC):")
    input_codes = input("Drivers: ").upper().replace(" ", "").split(",")

    telemetry_data = {}
    driver_shapes = {}
    team_colors = {}

    for i, code in enumerate(input_codes):
        try:
            telemetry, team_color = load_driver_lap(session_year, gp_name, session_type, code, return_team=True)
            telemetry_data[code] = telemetry
            driver_shapes[code] = MARKERS[i % len(MARKERS)]
            team_colors[code] = team_color
        except Exception as e:
            print(f"Error loading {code}: {e}")

    run_multi_driver_replay(telemetry_data, driver_shapes, team_colors)

if __name__ == "__main__":
    main()