import fastf1
import fastf1.plotting


def get_race_replay_telemetry(year, gp, session_type, drivers):
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, gp, session_type)
    session.load()

    telemetry_data = {}
    for code in drivers:
        try:
            lap = session.laps.pick_drivers(code).pick_fastest()
            tel = lap.get_telemetry().add_distance()
            team_name = session.get_driver(code).get("TeamName", "Unknown")
            try:
                team_color = fastf1.plotting.get_team_color(team_name, session)
            except:
                team_color = "#999999"
            
            telemetry_data[code] = {
                "X": tel['X'].tolist(),
                "Y": tel['Y'].tolist(),
                "team": team_name,
                "color": team_color,
            }
        except:
            telemetry_data[code] = {"X": [], "Y": []}

    return telemetry_data