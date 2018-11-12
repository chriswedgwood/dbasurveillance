import Plot from "react-plotly.js";
import React, { Component } from "react";
import PropTypes from "prop-types";
import Modal from "react-modal";
import axios from "axios";
import Prism from "prismjs";
import "../css/prism.css";
import { BootstrapTable, TableHeaderColumn } from "react-bootstrap-table";

const customStyles = {
  content: {
    height: "500px",
    width: "85%",
    top: "50%",
    left: "50%",
    right: "auto",
    bottom: "auto",
    marginRight: "-50%",
    transform: "translate(-50%, -50%)"
  }
};

const products = [
  {
    id: 1,
    name: "Product1",
    price: 120
  },
  {
    id: 2,
    name: "Product2",
    price: 80
  }
];

Modal.setAppElement("#app");

class Graph extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modalIsOpen: false,
      data: null
    };
    this.handlePlotlyClick = this.handlePlotlyClick.bind(this);
    this.openModal = this.openModal.bind(this);
    this.afterOpenModal = this.afterOpenModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
  }

  componentDidMount() {
    console.log("Prism highlight");
    Prism.highlightAll();
  }
  handlePlotlyClick(data) {
    //  console.log('handlePlotlyClick - Dashboard');

    let pts = "";
    let whoIsActiveDateTime = "";
    let instanceKey = 1;
    for (let i = 0; i < data.points.length; i++) {
      pts =
        "x = " +
        data.points[i].x +
        "\ny = " +
        data.points[i].y.toPrecision(4) +
        "\n\n";
      whoIsActiveDateTime = data.points[i].x;
      instanceKey = data.points[i].customdata;
    }

    console.log(whoIsActiveDateTime);
    console.log(instanceKey);

    axios
      .get("/api/whoisactive", {
        params: {
          date: whoIsActiveDateTime,
          instance_key: instanceKey
        }
      })
      .then(response => {
        this.setState({ modalIsOpen: true, data: response.data[0] });
      })
      .catch(error => {
        console.log(error);
      });
  }

  openModal() {
    this.setState({ modalIsOpen: true });
  }

  afterOpenModal() {
    // references are now sync'd and can be accessed.
    //this.subtitle.style.color = '#f00';
  }

  closeModal() {
    this.setState({ modalIsOpen: false });
  }

  render() {
    let table_data = [];

    const data = this.state.data;

    if (data !== null) {
      console.log("A");
      console.log(data);
      console.log("B");
      data.map((row, index) =>
        table_data.push({
          ParentSqlText: row[0],
          SqlText: row[1],
          CaptureDatetime: row[2]
        })
      );
    }

    return (
      <div>
        <Plot
          data={this.props.data}
          layout={this.props.layout}
          onClick={this.handlePlotlyClick}
          className="classddddclass"
        />
        <div>
          <Modal
            isOpen={this.state.modalIsOpen}
            onAfterOpen={this.afterOpenModal}
            onRequestClose={this.closeModal}
            style={customStyles}
            contentLabel="Example Modal"
          >
            <div>
              <BootstrapTable data={table_data} version="4">
                <TableHeaderColumn
                  width="33%"
                  isKey
                  dataField="ParentSqlText"
                  tdStyle={{ whiteSpace: "normal" }}
                >
                  ParentSqlText
                </TableHeaderColumn>
                <TableHeaderColumn
                  width="33%"
                  dataField="SqlText"
                  tdStyle={{ whiteSpace: "normal" }}
                >
                  SqlText
                </TableHeaderColumn>
                <TableHeaderColumn width="33%" dataField="CaptureDatetime">
                  CaptureDatetime
                </TableHeaderColumn>
              </BootstrapTable>
            </div>
          </Modal>
          <pre>
            <code className="language-javascript">
              {`
    onSubmit(e) {
      e.preventDefault();
      const job = {
        title: 'Developer',
        company: 'Facebook'
        };
      }
  `}
            </code>
          </pre>
        </div>
      </div>
    );
  }
}

Graph.propTypes = {
  data: PropTypes.array.isRequired,
  layout: PropTypes.object.isRequired
};

export default Graph;
