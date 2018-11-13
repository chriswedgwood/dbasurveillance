import React, {Component} from 'react';
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Graph from "./Graph";
import Select from 'react-select'
import SqlCountersGraph from "./SqlCountersGraph";
import ServerDropDown from './ServerDropDown'
import '../../../node_modules/bootstrap/dist/css/bootstrap.css';
import '../../../node_modules/react-bootstrap-table/dist/react-bootstrap-table-all.min.css';
import Plot from 'react-plotly.js';

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


  //shadows




  render() {
     var dataShadow = [
  {
    x: ['2018-02-01 00:00:00', '2018-02-01 01:00:00','2018-02-01 02:00:00','2018-02-01 03:00:00','2018-02-01 04:00:00',
        '2018-02-01 05:00:00', '2018-02-01 06:00:00','2018-02-01 07:00:00','2018-02-01 08:00:00','2018-02-01 09:00:00',
        '2018-02-01 10:00:00', '2018-02-01 11:00:00','2018-02-01 12:00:00','2018-02-01 13:00:00','2018-02-01 14:00:00',
        '2018-02-01 15:00:00', '2018-02-01 16:00:00','2018-02-01 17:00:00','2018-02-01 18:00:00','2018-02-01 19:00:00',
        '2018-02-01 20:00:00', '2018-02-01 21:00:00','2018-02-01 22:00:00','2018-02-01 23:00:00','2018-02-02 00:00:00',
        '2018-02-02 01:00:00', '2018-02-02 02:00:00','2018-02-02 03:00:00'],
    y: [14, 17, 12, 9, 90, 85, 12, 14, 12, 7, 11, 7, 18, 14, 14,
        16, 13, 7, 8, 14, 8, 3, 9, 9, 4, 13, 9, 6],
    mode: 'line',
    name: 'temperature'
  }/*,
         {
             x:['2015-02-04'],
             y:[0],
             mode: 'text',
             text: ['backup'],
             showlegend: false
         }*/
];

    var layoutShadow = {

    // to highlight the timestamp we use shapes and create a rectangular
    annotations: [
    {
      x: '2018-02-01 04:00:00',
      y: 100,
      xref: 'x',
      yref: 'y',
      text: 'Backups',
      showarrow: false,
      arrowhead: 7,
      ax: '2018-02-01 04:00:00',
      ay: -12
    }
  ],
    shapes: [
        // 1st highlight during Feb 4 - Feb 6
        {

            type: 'rect',
            // x-reference is assigned to the x-values
            xref: 'x',
            // y-reference is assigned to the plot paper [0,1]
            yref: 'paper',
            x0: '2018-02-01 03:00:00',
            y0: 0,
            x1: '2018-02-01 05:30:00',
            y1: 1,
            fillcolor: '#b2b2ff',
            opacity: 0.3,
            line: {
                width: 0
            }
        },

        // 2nd highlight during Feb 20 - Feb 23

        {
            type: 'rect',
            xref: 'x',
            yref: 'paper',
            x0: '2018-02-01 16:00:00',
            y0: 0,
            x1: '2018-02-01 17:00:00',
            y1: 1,
            fillcolor: '#d3d3d3',
            opacity: 0.2,
            line: {
                width: 0
            }
        }
    ],
    height: 800,
    width: 1000
}



    const isSelectedOption = this.state.selectedOption;
    const  lo  = {width: 1000, height: 800, title: 'CPU'};
    const  lo2  = {width: 1000, height: 800, title: 'Sql Counters'};
    const  lo3  = {width: 1000, height: 800, title: 'Wait Statistics'};

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
          render={data => <Graph data={data} layout={lo3}  />}
        />
        <div>
         <Plot
        data={[
          {
            x: [1, 2, 3],
            y: [2, 6, 3],
            type: 'scatter',
            mode: 'lines+points',
            marker: {color: 'red'},
          },
          {type: 'bar', x: [1, 2, 3], y: [2, 5, 3]},
        ]}
        layout={ {width: 1200, height: 800, title: 'A Fancy Plot'} }
         />
        </div>
          <div>
         <Plot
        data={dataShadow}
        layout={layoutShadow}
         />
        </div>

</div>

    );


  }
}


ReactDOM.render(
  <DashBoard />,
  document.getElementById('app')
);
