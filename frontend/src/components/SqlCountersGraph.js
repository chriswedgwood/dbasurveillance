import React, {Component} from 'react';
import Graph from './Graph'
import PropTypes from "prop-types";

class SqlCountersGraph extends Component {
    constructor(props) {
        super(props);
        //this.state = {data : this.props.data,lo: this.props.lo};
       //this.handleClick = this.handleClick.bind(this);
    }

/*    componentWillReceiveProps(props) {
    const { data } = this.props;
    this.setState(state => ({
      data: this.props.data
    }));

    }
    handleClick() {
    this.setState(state => ({
      data: state.data
    }));
  }*/

    render() {
        return (
            <div>
               <Graph data={this.props.data} layout={this.props.layout} />
            </div>
        );
    }
}

SqlCountersGraph.propTypes = {data: PropTypes.array.isRequired,
  layout:PropTypes.object.isRequired};

export default SqlCountersGraph;
