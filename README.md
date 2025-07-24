# F1 Stats

A comprehensive Formula 1 telemetry analysis tool that provides both command-line and web API interfaces for visualizing F1 driver performance data. Built with the FastF1 library to access official F1 telemetry data and create interactive race replays.

## Features

- **Race Replay Visualization**: Animated track replays showing multiple drivers' fastest laps
- **Multi-Driver Comparison**: Compare telemetry data from multiple drivers simultaneously
- **Web API**: RESTful API for accessing F1 data programmatically
- **Historical Data**: Access F1 data from 2018 onwards
- **Team Colors**: Authentic team colors for driver visualization
- **Interactive CLI**: Easy-to-use command-line interface for quick analysis

## Prerequisites

- Python 3.8 or higher
- Internet connection (for downloading F1 data)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BarTzipori/F1_Stats.git
   cd F1_Stats
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install additional dependencies for web API** (optional):
   ```bash
   pip install flask flask-cors pandas
   ```

## Usage

### Command Line Interface (CLI)

Run the main script to start an interactive F1 telemetry analysis session:

```bash
python main.py
```

**Example CLI Session**:
```
Enter driver codes (e.g. VER,HAM,LEC):
Drivers: VER,HAM,LEC
```

This will:
1. Load telemetry data for the specified drivers
2. Create an animated replay showing their fastest laps
3. Display the drivers moving around the track with team colors

**Available Driver Codes**: Standard F1 three-letter codes (e.g., VER, HAM, LEC, RUS, SAI, NOR, PIA, ALO, STR, BOT)

### Web API

Start the Flask web server for API access:

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/years` | GET | Get available F1 seasons | None |
| `/events` | GET | Get race events for a year | `year` (query param) |
| `/sessions` | GET | Get session types for an event | `year`, `gp` (query params) |
| `/drivers` | GET | Get drivers for a session | `year`, `gp`, `type` (query params) |
| `/telemetry` | POST | Get telemetry data for drivers | JSON body with `year`, `gp`, `type`, `drivers` |

#### API Examples

**Get available years**:
```bash
curl http://localhost:5000/years
```

**Get events for 2023**:
```bash
curl "http://localhost:5000/events?year=2023"
```

**Get drivers for Monaco 2023 Race**:
```bash
curl "http://localhost:5000/drivers?year=2023&gp=Monaco&type=R"
```

**Get telemetry data**:
```bash
curl -X POST http://localhost:5000/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2023,
    "gp": "Monaco",
    "type": "R",
    "drivers": ["VER", "HAM", "LEC"]
  }'
```

## Project Structure

```
F1_Stats/
├── main.py                 # CLI interface for race replay visualization
├── requirements.txt        # Python dependencies
├── backend/               # Web API components
│   ├── app.py            # Flask web server
│   └── graphs/
│       └── race_replay.py # Telemetry data processing for API
├── utils/                # Utility modules
│   ├── telemetry_loader.py # F1 data loading utilities
│   └── replay_plotter.py   # Race replay visualization
├── data/                 # Data cache directory (auto-created)
└── frontend/            # Frontend components (optional)
```

## Session Types

- **FP1**, **FP2**, **FP3**: Free Practice sessions
- **Q**: Qualifying session
- **SQ**: Sprint Qualifying (where applicable)
- **R**: Race session

## Configuration

The application uses the following default settings:
- **Default Year**: 2023
- **Default Grand Prix**: Monza
- **Default Session**: Race (R)
- **Cache Directory**: `data/cache` (CLI) or `cache` (API)

You can modify these defaults in the respective Python files or provide them via the API parameters.

## Data Source

This project uses the [FastF1](https://github.com/theOehrly/Fast-F1) library, which provides access to Formula 1 timing data and telemetry. The data includes:

- Lap times and sectors
- Telemetry data (speed, throttle, brake, etc.)
- Track position coordinates
- Driver and team information
- Session results

## Examples

### CLI Example Output
When running the CLI tool, you'll see:
1. A track layout in light gray
2. Colored dots representing each driver moving around the track
3. Driver codes labeled next to their positions
4. Animation showing the progression of their fastest laps

### API Response Example
```json
{
  "VER": {
    "X": [1234.5, 1235.2, ...],
    "Y": [567.8, 568.1, ...],
    "team": "Red Bull Racing Honda RBPT",
    "color": "#3671C6"
  },
  "HAM": {
    "X": [1234.1, 1234.8, ...],
    "Y": [567.5, 567.9, ...],
    "team": "Mercedes",
    "color": "#27F4D2"
  }
}
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure all dependencies are installed via `pip install -r requirements.txt`

2. **No Data Available**: Ensure you have an internet connection as F1 data is downloaded from official sources

3. **Driver Not Found**: Check that the driver code is correct and the driver participated in the specified session

4. **Session Not Available**: Verify the year, Grand Prix name, and session type are valid

### Performance Notes

- First-time data loading may take longer as FastF1 downloads and caches the data
- Subsequent runs for the same session will be faster due to caching
- The cache directory will grow over time as more sessions are accessed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source. Please check the repository for specific license information.

---

**Note**: This tool is for educational and analysis purposes. All F1 data is sourced from official Formula 1 timing systems via the FastF1 library.