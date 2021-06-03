import React, { Component } from 'react';

class Colorizer extends Component {
    state = {  }
    render() { 
        return ( 
            <div>
                <h2>Colorizer</h2>
                <form action="/action_page.php">
  <label for="img">Select image:</label>
  <input type="file" id="img" name="img" accept="image/*"/>
  <input type="submit"/>
</form>
            </div>
            

        );
    }
}
 
export default Colorizer;