import Plot from 'react-plotly.js';
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Modal from 'react-modal';


const customStyles = {
  content : {
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
            modalIsOpen:false
        }
        this.handlePlotlyClick = this.handlePlotlyClick.bind(this);
         this.openModal = this.openModal.bind(this);
        this.afterOpenModal = this.afterOpenModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }

    handlePlotlyClick(data){
      console.log('handlePlotlyClick - Dashboard');
      console.log('A');
      console.log(data);
    console.log('B');

     let pts = '';
          let whoIsActiveDateTime = '';
          for (let i = 0; i < data.points.length; i++) {
            pts = 'x = ' + data.points[i].x + '\ny = ' +
              data.points[i].y.toPrecision(4) + '\n\n';
            whoIsActiveDateTime = data.points[i].x;
          }
          console.log(whoIsActiveDateTime);

          this.setState({modalIsOpen: true});
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
        return (
           <div>
            <Plot
        data={this.props.data}
        layout={this.props.layout}
        onClick={this.handlePlotlyClick}
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
          <div>I am a modal</div>
          <form>
            <input />
            <button>tab navigation</button>
            <button>stays</button>
            <button>inside</button>
            <button>the modal</button>
          </form>
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
