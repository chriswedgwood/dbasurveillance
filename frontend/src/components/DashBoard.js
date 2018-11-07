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

class ServerDropDown extends React.Component
{
  constructor(props) {
    super(props);
    this.handleDropDownChange = this.handleDropDownChange.bind(this);
  }

  handleDropDownChange(e) {
    this.props.handleDropDownChange(e);
  }

  render() {
    return (
      <form>
         <Select  value={this.props.selectedOption} options={this.props.options} onChange={this.handleDropDownChange}  />
      </form>
    );
  }
}

class DashBoard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedOption:1,
      layout:{width: 1000, height: 800, title: 'Server 1'},
      cpuEndPoint:"api/cpu/1"
      };

    this.handleDropDownChange = this.handleDropDownChange.bind(this);

  }

  handleDropDownChange(selectedOption) {


    this.setState({
      selectedOption: selectedOption,
      layout:{width: 1000, height: 800, title: selectedOption.label},
      cpuEndPoint:"api/cpu/" + selectedOption.value

    });
  }

  render() {
    const isSelectedOption = this.state.selectedOption;
    const  lo  = {width: 1000, height: 800, title: 'CPU   '+isSelectedOption.label}

    if(isSelectedOption != null)
    {
    return (

      <div>
        <ServerDropDown
          selectedOption={this.state.selectedOption}
          options={options}
          handleDropDownChange={this.handleDropDownChange}

        />

        <DataProvider key={'cpu_'+this.state.selectedOption.value}
          endpoint={this.state.cpuEndPoint}
          render={data => <Graph data={data} layout={lo}  />}
        />
        <SqlCountersGraph data={'333'}/>


      </div>
    );
    }
    else
    {
      return (

      <div>
       XXXXXX


      </div>
    );
    }

  }
}


ReactDOM.render(
  <DashBoard />,
  document.getElementById('app')
);
