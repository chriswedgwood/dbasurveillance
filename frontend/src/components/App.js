import React, {Component} from 'react';
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Graph from "./Graph";
import Select from 'react-select'
import SqlCountersGraph from "./SqlCountersGraph";

const options = [
  { value: 1, label: 'Server1' },
  { value: 2, label: 'Server2' },
  { value: 3, label: 'Server3' }
]

const ServerDropDown = () => (
  <Select  value={selectedOption} options={options}  />
)

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            instance:1,
            selectedOption: null

        }
     this.handleChange = this.handleChange.bind(this);
    }

    handleChange = (selectedOption) => {
    this.setState({ instance: selectedOption.value });
    console.log(`Option selected:`, selectedOption);
  }
    render() {
        const { instance,selectedOption } = this.state;
        const url="api/cpu/" + instance;
        return (

           <div>
               <div>
              <Select
                value={selectedOption}
                onChange={this.handleChange}
                options={options}
                style={{width: `${(this.state.selectedOption.length) + 100}px`}}
              />
               </div>
               <div>
              <DataProvider key={this.state.instance}
          endpoint={url}
          render={data => <Graph data={data} />}
        />
               </div>

               <SqlCountersGraph />
      </div>
        );
    }
}

App.propTypes = {};

const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<App />, wrapper) : null;


