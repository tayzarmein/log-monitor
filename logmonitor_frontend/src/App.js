import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import OldGenGraph from "./OldGenGraph";
import DateTimePicker from 'react-datetime-picker';
import { sub } from 'date-fns';
import gclog from './gclog.json';


const LOGTYPES = {
  all: "all",
  newgenlog: "newgenlog",
  oldgenlog: "oldgenlog",
};

function App() {
  const [clickedLog, setClickedLog] = useState(LOGTYPES.oldgenlog);
  const logDivRef = useRef();
  const [endDateTime, setEndDateTime] = useState(new Date())
  const [startDateTime, setStartDateTime] = useState(sub(endDateTime, {weeks: 1}));
  const [dataState, setDataState] = useState("loading");
  const [data, setData] = useState([]);

  useEffect(() => {
    setTimeout(() => {
      setData(gclog);
      setDataState("ready");
      }, 1000);
  }, [])

  if (dataState === 'loading') {
    return <h2>Loading</h2>
  }

  return (
    <div>
      <h1>Status of Java Memory</h1>
      <p>Enter Range:</p>
      <DateTimePicker value={startDateTime} onChange={(v) => setStartDateTime(v)}/>
      <DateTimePicker value={endDateTime} onChange={(v) => setEndDateTime(v)}/>
      <button onClick={() => {
        setEndDateTime(new Date());
        setStartDateTime(sub(new Date(), {weeks: 1}));
      }}>Reset</button>

      <button onClick={() => setOneDay()}>1 Day</button>
      <button onClick={() => setOneWeek()}>1 Week</button>
      <button onClick={() => setOneMonth()}>1 Month</button>
      <button>Live</button>

      <p>
        <button
          onClick={() => setClickedLog(LOGTYPES.all)}
          className="graph-btn"
        >
          All
        </button>
        <button
          onClick={() => setClickedLog(LOGTYPES.oldgenlog)}
          className="graph-btn"
        >
          Old Gen
        </button>
        <button
          onClick={() => setClickedLog(LOGTYPES.newgenlog)}
          className="graph-btn"
        >
          New Gen
        </button>
      </p>
      {renderGraph()}
      <div ref={logDivRef} />
    </div>
  );

  function renderGraph() {
    switch (clickedLog) {
      case LOGTYPES.newgenlog:
        return <p>This is new Gen graph</p>;

      case LOGTYPES.oldgenlog:
        return <OldGenGraph data={data} {...{startDateTime, endDateTime}} />;

      case LOGTYPES.all:
        return <p>This is all graph</p>;

      default:
        break;
    }
  }

  function setOneDay() {
    let now = new Date();
    setEndDateTime(now);
    setStartDateTime(sub(now, {days: 1}))
  }

  function setOneWeek() {
    let now = new Date();
    setEndDateTime(now);
    setStartDateTime(sub(now, {weeks: 1}))
  }

  function setOneMonth() {
    let now = new Date();
    setEndDateTime(now);
    setStartDateTime(sub(now, {months: 1}))
  }

}

export default App;
