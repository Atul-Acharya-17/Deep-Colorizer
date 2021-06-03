import React, { Component } from 'react'
import axios from 'axios';  

class MainMenu extends Component {


    componentDidMount(){
        this.getText();
    }

    state = {
        text: 'Text'
    }

    getText = () => {
        axios.get('http://localhost:5000/predict').then(response => {
            console.log(response.data)
            this.setState({text: response.data})
        }
        )
    }

    render() {
        return <div>
            <h3>
                Deep Colorizer
            </h3>
            <h3>
                {this.state.text}
            </h3>
        </div>
    }
}

export default MainMenu;