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
    this.state = {options:options,
                    error: null,
      isLoaded: false,}
    this.handleDropDownChange = this.handleDropDownChange.bind(this);

  }

  handleDropDownChange(e) {
    this.props.handleDropDownChange(e);
  }

  componentDidMount() {
    fetch("/api/instances/?format=json")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            options: result
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }


  render() {
    return (
      <form>
         <Select  value={this.props.selectedOption} options={this.state.options} onChange={this.handleDropDownChange}  />
      </form>
    );
  }
}


export default ServerDropDown;
