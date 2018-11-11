import Plot from 'react-plotly.js';
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Modal from 'react-modal';
import axios from 'axios';

const customStyles = {
  content : {
      height: '500px',
    width: '85%',
    top                   : '50%',
    left                  : '50%',
    right                 : 'auto',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)'
  }
};

Modal.setAppElement('#app')

class Graph extends Component {

    constructor(props) {
        super(props);
        this.state = {
            modalIsOpen:false,
            data:null
        }
        this.handlePlotlyClick = this.handlePlotlyClick.bind(this);
         this.openModal = this.openModal.bind(this);
        this.afterOpenModal = this.afterOpenModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }

    handlePlotlyClick(data){
    //  console.log('handlePlotlyClick - Dashboard');


     let pts = '';
          let whoIsActiveDateTime = '';
          let instanceKey = 1;
          for (let i = 0; i < data.points.length; i++) {
            pts = 'x = ' + data.points[i].x + '\ny = ' +
              data.points[i].y.toPrecision(4) + '\n\n';
            whoIsActiveDateTime = data.points[i].x;
            instanceKey = data.points[i].customdata;

          }

        console.log(whoIsActiveDateTime);
          console.log(instanceKey);



          axios.get('/api/whoisactive', {
           params: {
            date:whoIsActiveDateTime,instance_key:instanceKey
                }
              })
              .then(response => {


                this.setState({modalIsOpen: true,data:response.data});


              })
              .catch((error)=>{
       console.log(error);
    });

  }

  openModal() {
    this.setState({modalIsOpen: true});


  }

  afterOpenModal() {
    // references are now sync'd and can be accessed.
    this.subtitle.style.color = '#f00';


  }

  closeModal() {
    this.setState({modalIsOpen: false});
  }



   render() {

        const data = this.state.data;

        const rows = data.map((row) =>
            <tr><td>{row[0]}</td></tr>
);


        return (
           <div>
            <Plot
        data={this.props.data}
        layout={this.props.layout}
        onClick={this.handlePlotlyClick}
        className='classddddclass'
            />
           <div>
            <Modal
          isOpen={this.state.modalIsOpen}
          onAfterOpen={this.afterOpenModal}
          onRequestClose={this.closeModal}
          style={customStyles}
          contentLabel="Example Modal"
            >

          <h2 ref={subtitle => this.subtitle = subtitle}>Hello</h2>
            <button onClick={this.closeModal}>close</button>
          <div>I am a modal2</div>
<table>{rows}</table>
        </Modal>
          </div>
           </div>
            )
    }
}

Graph.propTypes = {
  data: PropTypes.array.isRequired,
  layout:PropTypes.object.isRequired
};


export default Graph;
