import React, { useEffect, useState } from "react";
import axios from "axios";
import Select from "react-select";

function App() {
  const [years, setYears] = useState([]);
  const [events, setEvents] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [selectedYear, setSelectedYear] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [selectedSession, setSelectedSession] = useState(null);
  const [drivers, setDrivers] = useState([]);
  const [selectedDrivers, setSelectedDrivers] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/years").then((res) => {
      setYears(res.data.years);
    });
  }, []);

  useEffect(() => {
    if (selectedYear) {
      axios
        .get(`http://localhost:5000/events?year=${selectedYear}`)
        .then((res) => {
          setEvents(res.data.events);
        });
    }
  }, [selectedYear]);

  useEffect(() => {
    if (selectedYear && selectedEvent) {
      axios
        .get(
          `http://localhost:5000/sessions?year=${selectedYear}&gp=${selectedEvent}`
        )
        .then((res) => {
          setSessions(res.data.sessions);
        });
    }
  }, [selectedEvent]);

  useEffect(() => {
    if (selectedYear && selectedEvent && selectedSession) {
      axios
        .get(
          `http://localhost:5000/drivers?year=${selectedYear}&gp=${selectedEvent}&type=${selectedSession}`
        )
        .then((res) => {
          setDrivers(res.data.drivers);
        });
    }
  }, [selectedSession]);

  const runReplay = () => {
    if (!selectedYear || !selectedEvent || !selectedSession) return;
    axios
      .post("http://localhost:5000/telemetry", {
        year: selectedYear,
        gp: selectedEvent,
        type: selectedSession,
        drivers: selectedDrivers.map((d) => d.code),
      })
      .then((res) => {
        console.log("Telemetry:", res.data);
        // TODO: Draw graph here
      });
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>F1 Race Replay</h1>

      <label>Year:</label>
      <Select
        options={years.map((y) => ({ label: y.toString(), value: y }))}
        onChange={(option) => setSelectedYear(option.value)}
      />

      <label>Event:</label>
      <Select
        options={events.map((gp) => ({ label: gp, value: gp }))}
        onChange={(option) => setSelectedEvent(option.value)}
      />

      <label>Session:</label>
      <Select
        options={sessions.map((s) => ({ label: s, value: s }))}
        onChange={(option) => setSelectedSession(option.value)}
      />

      <label>Drivers:</label>
      <Select
        isMulti
        options={drivers.map((d) => ({
          label: `${d.name} (${d.code})`,
          value: d.code,
          code: d.code,
        }))}
        onChange={(selected) => setSelectedDrivers(selected)}
      />

      <button onClick={runReplay} style={{ marginTop: "1rem" }}>
        Run Replay
      </button>
    </div>
  );
}

export default App;