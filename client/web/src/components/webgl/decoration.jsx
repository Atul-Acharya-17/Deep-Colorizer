import React, { Component } from 'react';
import * as THREE from "three";
import decorationTexture from '../../static/texture/NormalMap.png'
import './style.css';

import example1 from '../../static/texture/black_and_white/example1.jpeg';
import example2 from '../../static/texture/black_and_white/example3.jpg';
import example3 from '../../static/texture/black_and_white/example3.jpg';
import example4 from '../../static/texture/black_and_white/example4.jpeg';
import example5 from '../../static/texture/black_and_white/example5.jpeg';
import example6 from '../../static/texture/black_and_white/example6.jpeg';

import color1 from '../../static/texture/colors/example1.jpeg';
import color2 from '../../static/texture/colors/example2.jpg';
import color3 from '../../static/texture/colors/example3.jpg';
import color4 from '../../static/texture/colors/example4.jpeg';
import color5 from '../../static/texture/colors/example5.jpeg';
import color6 from '../../static/texture/colors/example6.jpeg';

class Decoration extends Component {
    componentDidMount() {
        var textureLoader = new THREE.TextureLoader()
        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
        var renderer = new THREE.WebGLRenderer({alpha:true});
        renderer.setSize( window.innerWidth, window.innerHeight );
        this.mount.appendChild( renderer.domElement );
      
        const geometry = new THREE.SphereBufferGeometry( .5, 34, 34 );
        const cubeGeometry = new THREE.BoxGeometry(1., 1., 1.);
        const cube2Geometry = new THREE.BoxGeometry(1., 1., 1.);
        // Materials
  
          const material = new THREE.MeshStandardMaterial({normalMap: textureLoader.load(decorationTexture)})
          material.color = new THREE.Color(0x292929)
          material.metalness = 0.5
          material.roughness = 0.5

          const cubeMaterials1 = [
            new THREE.MeshStandardMaterial({map: textureLoader.load(example1)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(example2)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(example3)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(example4)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(example5)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(example6)}),  
          ]

          const cubeMaterials2 = [
            new THREE.MeshStandardMaterial({map: textureLoader.load(color1)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(color2)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(color3)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(color4)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(color5)}),
            new THREE.MeshStandardMaterial({map: textureLoader.load(color6)}),  
          ]


          // Mesh
          const sphere = new THREE.Mesh(geometry,material)
          scene.add(sphere)
          sphere.position.set(0, 0.41, 0)
          // Lights

          const cube = new THREE.Mesh(cubeGeometry, cubeMaterials1);
          scene.add(cube)
          cube.position.set(-1.8, -1.5, -1.75) 

          const cube2 = new THREE.Mesh(cube2Geometry, cubeMaterials2);
          scene.add(cube2)
          cube2.position.set(1.8, -1.5, -1.75) 

          const pointLight = new THREE.PointLight(0xffffff)//0xe1ff, 2)
          pointLight.position.set(2.13, -3.4, -1)
          pointLight.intensity = 0.2
          pointLight.distance = 0
          scene.add(pointLight)
  
          const pointLight2 = new THREE.PointLight(0xffffff)//0x440000, 2)
          pointLight2.position.set(-1.86, 2.41, -1.65)
          pointLight2.intensity = 2
          pointLight2.distance = 0
          scene.add(pointLight2)

          const pointLight3 = new THREE.PointLight(0xffffff)//0x440000, 2)
          pointLight3.position.set(-1.8, -1.5, -1.0)  
          pointLight3.intensity = 2
          pointLight3.distance = 2
          scene.add(pointLight3)
          camera.position.z = 2;

          const pointLight4 = new THREE.PointLight(0xffffff)//0x440000, 2)
          pointLight4.position.set(1.8, -1.5, -1.0)  
          pointLight4.intensity = 1
          pointLight4.distance = 3
          scene.add(pointLight4)

  
        var animate = function () {
            requestAnimationFrame( animate );
            sphere.rotation.x += 0.0005;
            sphere.rotation.y += 0.007;
            sphere.rotation.z += 0.0005;
            cube.rotation.x += 0.005
            cube.rotation.y += 0.01
            cube.rotation.z -= 0.005
            cube2.rotation.x -= 0.005
            cube2.rotation.y -= 0.01
            cube2.rotation.z += 0.005
            renderer.render( scene, camera );

            
        };
        animate();
    }
    render() {
        return (
            <div>
                <div class="container">
                    <h1>DEEP COLORIZER</h1>
                </div>
                <div ref={ref => (this.mount = ref)} class="webgl"/>
            </div>
            
                
            
        )
    }
  }

  export default Decoration

