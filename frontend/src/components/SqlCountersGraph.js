import React, {Component} from 'react';
import Graph from './Graph'

class SqlCountersGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {data : this.props.data};
        this.handleClick = this.handleClick.bind(this);
    }

    componentWillReceiveProps(props) {
    const { data } = this.props;
    this.setState(state => ({
      data: this.props.data
    }));

    }
    handleClick() {
    this.setState(state => ({
      data: state.data+"1"
    }));
  }

    render() {
        return (
            <div>
                <button onClick={this.handleClick}>
        {this.state.data }
      </button>
            </div>
        );
    }
}

SqlCountersGraph.propTypes = {};

export default SqlCountersGraph;
