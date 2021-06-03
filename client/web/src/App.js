import React, { Component } from 'react'

import Decoration from "./components/webgl/decoration";
import Colorizer from "./components/colorizer/colorizer";

class App extends Component {
//   componentDidMount() {
//       var textureLoader = new THREE.TextureLoader()
//       var scene = new THREE.Scene();
//       var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
//       var renderer = new THREE.WebGLRenderer({alpha:true});
//       renderer.setSize( window.innerWidth, window.innerHeight );
//       this.mount.appendChild( renderer.domElement );
    
//       const geometry = new THREE.SphereBufferGeometry( .5, 34, 34 );

// // Materials

//         const material = new THREE.MeshStandardMaterial({normalMap: textureLoader.load(texture)})
//         material.color = new THREE.Color(0x292929)
//         material.metalness = 0.7
//         material.roughness = 0.3
//         // Mesh
//         const sphere = new THREE.Mesh(geometry,material)
//         scene.add(sphere)

//         // Lights

//         const pointLight = new THREE.PointLight(0xe1ff, 2)
//         pointLight.position.set(2.13, -3, -2)
//         pointLight.intensity = 0.5
//         scene.add(pointLight)

//         const pointLight2 = new THREE.PointLight(0x440000, 2)
//         pointLight2.position.set(-1.86, 1, -1.65)
//         pointLight2.intensity = 5
//         scene.add(pointLight2)
//         camera.position.z = 2;

//       var animate = function () {
//           requestAnimationFrame( animate );
//           sphere.rotation.x += 0.0005;
//           sphere.rotation.y += 0.007;
//           sphere.rotation.z += 0.0005;
//           renderer.render( scene, camera );
//       };
//       animate();
//   }
  render() {
      return (
          //<div ref={ref => (this.mount = ref)} />
          <div>
              <Decoration/>
              <Colorizer/>
          </div>
          
      )
  }
}

export default App;
