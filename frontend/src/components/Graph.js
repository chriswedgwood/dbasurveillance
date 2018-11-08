import React from 'react';
import Plot from 'react-plotly.js';
import PropTypes from "prop-types";



const Graph = ({ data, layout }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : ( <Plot
        data={data}
        layout={layout}
      />
  );

Graph.propTypes = {
  data: PropTypes.array.isRequired,
  layout:PropTypes.object.isRequired
};

export default Graph;