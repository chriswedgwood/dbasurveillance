import React, {Component} from 'react';
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Graph from "./Graph";
import Select from 'react-select'


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
      selectedOption:null,
      layout:{width: 1000, height: 800, title: 'Server 1'}
      };

    this.handleDropDownChange = this.handleDropDownChange.bind(this);

  }

  handleDropDownChange(selectedOption) {
    this.setState({
      selectedOption: selectedOption,
      layout:{width: 1000, height: 800, title: selectedOption.label}
    });
  }

  render() {
    const isSelectedOption = this.state.selectedOption;
    const server =  this.state.selectedOption ? this.state.selectedOption.value : 1
    return (

      <div>
        <ServerDropDown
          selectedOption={this.state.selectedOption}
          options={options}
          handleDropDownChange={this.handleDropDownChange}

        />

        <DataProvider //key={this.state.instance}
          endpoint={"api/cpu/" + server }
          render={data => <Graph data={data} layout={this.state.layout} />}
        />



      </div>
    );
  }
}


ReactDOM.render(
  <DashBoard />,
  document.getElementById('app')
);
