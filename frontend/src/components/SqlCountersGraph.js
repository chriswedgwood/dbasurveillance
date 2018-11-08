import React, {Component} from 'react';
import Graph from './Graph'
import PropTypes from "prop-types";
import SqlCounterDropDown from "./SqlCounterDropDown"

class SqlCountersGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {data:this.props.data,isLoaded: false};
        this.handleDropDownChange = this.handleDropDownChange.bind(this);
    }

  handleDropDownChange(selectedOption) {

    console.log('handledropdownchangeSQLCountersGraph');
    console.log(selectedOption);

    const endPoint = 'api/sqlcounters/1/?format=json&'+selectedOption.map(x => `sqlCounters[]=${x.label}`).join('&');
    console.log(endPoint);
    console.log(this.props.server);

     fetch(endPoint)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            data: result
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
            <div>
               <SqlCounterDropDown handleDropDownChange={this.handleDropDownChange}  />
               <Graph data={this.state.data} layout={this.props.layout} />
            </div>
        );
    }
}

SqlCountersGraph.propTypes = {data: PropTypes.array.isRequired,
  layout:PropTypes.object.isRequired,server:PropTypes.number.isRequired};

export default SqlCountersGraph;
