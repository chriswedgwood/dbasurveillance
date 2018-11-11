import React, {Component} from 'react';
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Graph from "./Graph";
import Select from 'react-select'
import SqlCountersGraph from "./SqlCountersGraph";
import ServerDropDown from './ServerDropDown'

class DashBoard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedOption:1,
      layout:{width: 1000, height: 800, title: 'Server 1'},
      cpuEndPoint:"api/cpu/1",
      sqlCountersEndPoint:"api/sqlcounters/1",
      waitsEndPoint:"api/waitstats/1",
      whoisActiveDateTime:null,


      };

    this.handleDropDownChange = this.handleDropDownChange.bind(this);

  }





  handleDropDownChange(selectedOption) {


    this.setState({
      selectedOption: selectedOption,
      layout:{width: 1000, height: 800, title: selectedOption.label},
      cpuEndPoint:"api/cpu/" + selectedOption.value,
      sqlCountersEndPoint:"api/sqlcounters/" + selectedOption.value,
      waitsEndPoint:"api/waitstats/" + selectedOption.value,



    });
  }



  render() {
    const isSelectedOption = this.state.selectedOption;
    const  lo  = {width: 1000, height: 800, title: 'CppU',xxx:'xxx'};
    const  lo2  = {width: 1000, height: 800, title: 'SC'};

    return (

      <div>
        <ServerDropDown
          selectedOption={this.state.selectedOption}
          handleDropDownChange={this.handleDropDownChange}

        />

        <DataProvider key={'cpu_'+this.state.selectedOption.value}
          endpoint={this.state.cpuEndPoint}
          render={data => <Graph data={data} layout={lo}  handlePlotlyClick={this.handlePlotlyClick}  />}
        />
        <DataProvider key={'sql_counters_'+this.state.selectedOption.value}
          endpoint={this.state.sqlCountersEndPoint}
          render={data => <SqlCountersGraph data={data} layout={lo2} server={this.state.selectedOption} />}
        />
        <DataProvider key={'waits_'+this.state.selectedOption.value}
          endpoint={this.state.waitsEndPoint}
          render={data => <Graph data={data} layout={lo}  />}
        />


      </div>
    );


  }
}


ReactDOM.render(
  <DashBoard />,
  document.getElementById('app')
);
