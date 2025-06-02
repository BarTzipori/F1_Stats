import warnings
import fastf1
from fastf1.plotting import TEAM_COLORS

warnings.filterwarnings("ignore", category=FutureWarning)
fastf1.Cache.enable_cache('data/cache')

def load_driver_lap(year, gp_name, session_type, driver_code, return_team=False):
    session = fastf1.get_session(year, gp_name, session_type)
    session.load()

    fastest_lap = session.laps.pick_drivers(driver_code).pick_fastest()
    telemetry = fastest_lap.get_telemetry().add_distance()

    if return_team:
        driver_info = session.get_driver(driver_code)
        team_name = driver_info['TeamName']
        team_color = TEAM_COLORS.get(team_name, 'gray')
        return telemetry, team_color

    return telemetry