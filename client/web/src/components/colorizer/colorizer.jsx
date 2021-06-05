import React, { Component } from 'react';
import './style.css';
import defaultImage from '../../static/texture/default.png';

class Colorizer extends Component {

    constructor(props) {
        super(props);
        this.handleUpload = this.handleUpload.bind(this);
    }

    state = { 
        image: defaultImage,
        file: null
     }
    render() { 
        return ( 
            <div className="colorizer">
                <h2>COLORIZER</h2>
                <img src={this.state.image} width="300" height="300"/>
                <label>
                <input type='file' onChange={this.handleUpload} />
                <text>Upload Image</text>
                </label>
                <button type="button" onClick={this.colorizeImage}>
                    <text className="predict">Colorize</text>
                </button>
                
            </div>
            

        );
    }

    handleUpload = (event) => {
        try {
            this.setState({
                image: URL.createObjectURL(event.target.files[0]),
                file: event.target.files[0]
              })
          }
        catch(error) {
            this.setState({
                image: defaultImage,
                file: null
              })
        }
      }

    colorizeImage = (event) => {
        event.preventDefault()
        const data = new FormData();
        data.append("image", this.state.file);
        fetch('http://localhost:5000/colorize', {
            method: 'POST',
            body: data,
            type: "application/json",
        }).then((response) => {
            console.log(response)
            response.blob()
            .then((blob) => {
                console.log(blob)
                let url = URL.createObjectURL(blob);
                this.setState({
                    image: url,
                  })
            })
            });
    }
    
}
 
export default Colorizer;