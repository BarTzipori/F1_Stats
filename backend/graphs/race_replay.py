import fastf1
from fastf1.plotting import TEAM_COLORS


def get_race_replay_telemetry(year, gp, session_type, drivers):
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, gp, session_type)
    session.load()

    telemetry_data = {}
    for code in drivers:
        try:
            lap = session.laps.pick_drivers(code).pick_fastest()
            tel = lap.get_telemetry().add_distance()
            telemetry_data[code] = {
                "X": tel['X'].tolist(),
                "Y": tel['Y'].tolist(),
                "team": session.get_driver(code).get("TeamName", "Unknown"),
                "color": TEAM_COLORS.get(session.get_driver(code).get("TeamName", "Unknown"), "#999999"),
            }
        except:
            telemetry_data[code] = {"X": [], "Y": []}

    return telemetry_data