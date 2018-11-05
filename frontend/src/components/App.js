import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Graph from "./Graph";


const App = () => (
  <DataProvider endpoint="api/cpu/"
                render={data => <Graph data={data} />} />
);

const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<App />, wrapper) : null;