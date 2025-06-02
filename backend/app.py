# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import fastf1
from fastf1.plotting import TEAM_COLORS
from datetime import datetime
from graphs.race_replay import get_race_replay_telemetry

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="*", methods=["GET", "POST", "OPTIONS"])

fastf1.Cache.enable_cache('cache')

@app.route("/years", methods=["GET"])
def get_years():
    current_year = datetime.now().year
    return jsonify({"years": list(range(2018, current_year + 1))})

@app.route("/events", methods=["GET"])
def get_events():
    year = int(request.args.get("year", 2023))
    events = fastf1.get_event_schedule(year)
    event_names = events['EventName'].tolist()
    return jsonify({"events": event_names})

@app.route("/sessions", methods=["GET"])
def get_sessions():
    year = int(request.args.get("year", 2023))
    gp = request.args.get("gp", "Monza")
    event = fastf1.get_event_schedule(year)
    match = event[event['EventName'] == gp]
    if match.empty:
        return jsonify({"sessions": []})
    row = match.iloc[0]
    sessions = []
    for s in ["FP1", "FP2", "FP3", "Q", "SQ", "R"]:
        if not pd.isna(row.get(s + "Date")):
            sessions.append(s)
    return jsonify({"sessions": sessions})

@app.route("/drivers", methods=["GET"])
def get_drivers():
    year = int(request.args.get("year", 2023))
    gp = request.args.get("gp", "Monza")
    session_type = request.args.get("type", "R")
    session = fastf1.get_session(year, gp, session_type)
    session.load()

    drivers = []
    for drv in session.drivers:
        info = session.get_driver(drv)
        team = info.get('TeamName', 'Unknown')
        color = TEAM_COLORS.get(team, '#999999')
        name = info.get('FullName') or f"{info.get('GivenName', '')} {info.get('FamilyName', '')}".strip()
        drivers.append({
            "code": drv,
            "name": name,
            "team": team,
            "color": color
        })

    return jsonify({"drivers": drivers})

@app.route("/telemetry", methods=["POST", "OPTIONS"])
def get_telemetry():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()
    year = data.get("year", 2023)
    gp = data.get("gp", "Monza")
    session_type = data.get("type", "R")
    drivers = data.get("drivers", [])

    session = fastf1.get_session(year, gp, session_type)
    session.load()

    return jsonify(get_race_replay_telemetry(year, gp, session_type, drivers))

if __name__ == "__main__":
    app.run(debug=True)