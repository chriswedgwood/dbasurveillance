import React from 'react';
import Plot from 'react-plotly.js';
import PropTypes from "prop-types";



const Graph = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : ( <Plot
        data={data}
        layout={ {width: 1000, height: 800, title: 'A Fancy Plot'}}
      />
  );

Graph.propTypes = {
  data: PropTypes.array.isRequired
};

export default Graph;