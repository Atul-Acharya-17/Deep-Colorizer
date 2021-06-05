import React, { Component } from 'react'

import Decoration from "./components/webgl/decoration";
import Colorizer from "./components/colorizer/colorizer";

class App extends Component {
  render() {
      return (
          <div>
              <Decoration/>
              <Colorizer/>
          </div>
          
      )
  }
}

export default App;
