import React, {Component} from 'react';
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Graph from "./Graph";


class App extends Component {
    render() {
        return (
           <span>
        <DataProvider
          endpoint="api/cpu/"
          render={data => <Graph data={data} />}
        />
      </span>
        );
    }
}

App.propTypes = {};

const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<App />, wrapper) : null;
