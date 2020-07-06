import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import ReactDOM from "react-dom";
import * as d3 from "d3";

const LOGTYPES = {
  all: "all",
  newgenlog: "newgenlog",
  oldgenlog: "oldgenlog",
};

function App() {
  const [selectedLog, setSelectedLog] = useState(LOGTYPES.all);
  // const [showLog, setShowLog] = useState(false);
  const logDivRef = useRef();
  const [startDateTime, setStartDateTime] = '';
  const [endDateTime, setEndDateTime] = '';

  return (
    <div>
      <h1>Dashboard</h1>
      <p>
        Select Log Type :
        <select
          value={selectedLog}
          onChange={(e) => setSelectedLog(e.target.value)}
        >
          <option value={LOGTYPES.all}>All</option>
          <option value={LOGTYPES.oldgenlog}>OldGen</option>
          <option value={LOGTYPES.newgenlog}>NewGen</option>
        </select>
      </p>
      <p>
        Start datetime :
        <input value={startDateTime} onChange={(e) => setStartDateTime(e.target.value)} />
        (yyyy-mm-dd hh:mm:ss)
        <span>Leave Blank for all time</span>
      </p>
      <p>
        End datetime :
        <input value={endDateTime} onChange={(e) => setEndDateTime(e.target.value)} />
        (yyyy-mm-dd hh:mm:ss)
        <span>Leave Blank for all time</span>
      </p>
      <p>
        <button onClick={() => renderResult()}>GET</button>
      </p>
      <div ref={logDivRef} />
    </div>
  );

  function renderResult() {
    switch (selectedLog) {
      case LOGTYPES.all:
        ReactDOM.render(<All />, logDivRef.current);
        return;

      case LOGTYPES.newgenlog:
        ReactDOM.render(<NewGenLog />, logDivRef.current);
        return;

      case LOGTYPES.oldgenlog:
        ReactDOM.render(<OldGenLog />, logDivRef.current);
        return;

      default:
        return null;
    }
  }
}

function NewGenLog() {
  return (
    <div>
      <h3>This is a log of Old gen space in GC</h3>
      <img
        src="https://via.placeholder.com/800x750?text=new+gen+log"
        alt="new-gen-log"
      />
    </div>
  );
}

function OldGenLog() {
  return (
    <div>
      <h3>This is a log of New gen space in GC</h3>
      <img
        src="https://via.placeholder.com/800x750?text=old+gen+log"
        alt="old-gen-log"
      />
    </div>
  );
}

function All() {
  const data = [
    {
      date: "1-May-12",
      close: 58.13,
    },
    {
      date: "30-Apr-12",
      close: 53.98,
    },
    {
      date: "27-Apr-12",
      close: 67,
    },
    {
      date: "26-Apr-12",
      close: 89.7,
    },
    {
      date: "25-Apr-12",
      close: 99,
    },
    {
      date: "24-Apr-12",
      close: 130.28,
    },
    {
      date: "23-Apr-12",
      close: 166.7,
    },
    {
      date: "20-Apr-12",
      close: 234.98,
    },
    {
      date: "19-Apr-12",
      close: 345.44,
    },
    {
      date: "18-Apr-12",
      close: 443.34,
    },
    {
      date: "17-Apr-12",
      close: 543.7,
    },
    {
      date: "16-Apr-12",
      close: 580.13,
    },
    {
      date: "13-Apr-12",
      close: 605.23,
    },
    {
      date: "12-Apr-12",
      close: 622.77,
    },
    {
      date: "11-Apr-12",
      close: 626.2,
    },
    {
      date: "10-Apr-12",
      close: 628.44,
    },
    {
      date: "9-Apr-12",
      close: 636.23,
    },
    {
      date: "5-Apr-12",
      close: 633.68,
    },
    {
      date: "4-Apr-12",
      close: 624.31,
    },
    {
      date: "3-Apr-12",
      close: 629.32,
    },
    {
      date: "2-Apr-12",
      close: 618.63,
    },
    {
      date: "30-Mar-12",
      close: 599.55,
    },
    {
      date: "29-Mar-12",
      close: 609.86,
    },
    {
      date: "28-Mar-12",
      close: 617.62,
    },
    {
      date: "27-Mar-12",
      close: 614.48,
    },
    {
      date: "26-Mar-12",
      close: 606.98,
    },
  ];

  useEffect(() => {
    const margin = {
      top: 20,
      right: 20,
      bottom: 30,
      left: 50,
    };

    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const parseTime = d3.timeParse("%d-%b-%y");

    const x = d3.scaleTime().range([0, width]);
    const y = d3.scaleLinear().range([height, 0]);

    const valueLine = d3
      .line()
      .x((d) => x(d.date))
      .y((d) => y(d.close));

    const svg = d3
      .select("#resultDiv")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    data.forEach((d) => {
      d.date = parseTime(d.date);
      d.close = +d.close;
    });

    console.log("data=", data);

    x.domain(d3.extent(data, (d) => d.date));
    y.domain([0, d3.max(data, (d) => d.close)]);

    svg.append("path").data([data]).attr("class", "line").attr("d", valueLine);

    svg
      .append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    svg.append("g").call(d3.axisLeft(y));
  }, [data]);

  return (
    <div>
      <h3>This is a log of GC</h3>
      <div
        id="resultDiv"
      />
    </div>
  );
}

export default App;
