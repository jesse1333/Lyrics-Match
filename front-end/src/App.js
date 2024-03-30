import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './App.css'; // Import your CSS file
import logo from './assets/microphone.svg'

function App() {
  // Orange Border Component
  const OrangeBorder = {
    top: '0', 
    left: '0',
    width: '100%',
    height: '40vh',
    backgroundColor: 'orange',
    position: 'absolute', 
    marginTop: '0',
    zIndex: '-1'
  };

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       axios.post('/', { userLyrics: data}) // Assumes React is running on the same server as Flask
  //       .then(response => {
  //         setSongObjects(response.data)
  //         console.log("Data receieved " + songObjects)
  //       })
  //       .catch(error => {
  //         console.error('Error fetching data:', error);
  //       });
        
  //       // Handle the response data here
  //       console.log(response.data);
  //     } catch (error) {
  //       // Handle any errors here
  //       console.error('Error fetching data:', error);
  //     }
  //   };

  //   // Call the function to fetch data when the component mounts
  //   fetchData();
  // }, []);
  
  // Search Bar Component (Sends Axios Data)
  const SearchBar = (left) => {
    const [data, setData] = useState()
    const [songObjects, setSongObjects] = useState()

    const inputStyle= { position: 'absolute', 
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)'
    }

    const handleKeyDown = (event) => {
      if (event.key === 'Enter') {
        event.preventDefault(); 
        document.getElementById("lyrics-input").value = "";

        // ADD CODE THAT SENDS DATA UP TO BACKEND
        axios.post('/', { userLyrics: data}) // Assumes React is running on the same server as Flask
        .then(response => {
          setSongObjects(response.data)
          console.log("Data receieved " + songObjects)
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
        setData('')
      }
    }

    const handleChange = (event) => {
      setData(event.target.value);
    }

    return (
      <div class="form__group field" style={inputStyle}>
        <input type="input" onChange={handleChange} onKeyDown={handleKeyDown} class="form__field" placeholder="lyrics" name="lyrics-input" id='lyrics-input' required />
        <label for="lyrics-input" class="form__label">Lyrics:</label>
        <h1> {data} </h1>
      </div>
    );
  };


  // Album Component
  const Album = ({imageSrc, left, right, flex}) => {
    const albumStyle = {
      left: left,
      right: right,
      top: '55%',
      flex: flex,
    };

    return (
      <div className="album-container">
      <img src={imageSrc} style={albumStyle} alt="Album Cover" />
    </div>
    );
  };

  const [album_1, set_album_1] = useState()
  const [album_2, set_album_2] = useState()
  const [album_3, set_album_3] = useState()
  
  // Website Render Method
  return (
    <div className="App">
    <div className="orange-border" style={{...OrangeBorder }}></div>

    <div className="title-container" style={{position: 'absolute'}}>
      <h1 style={{position: 'relative', fontSize: 40, left: 30}}> Lyrics Match </h1>
      <img src={logo} alt="Microphone Logo" style={{height: 40, width: 40, position: 'relative', left: 190, top: -70}}/>
    </div>  

      <div className="search-bar-container">
        <SearchBar></SearchBar>
      </div>
      <div className="albums-container">
      <Album></Album>
      <Album></Album>
      <Album></Album>

      </div>
    </div>
  );
}

export default App;





// // import logo from './logo.svg';
// // import './App.css';

// // function App() {
// //   return (
// //     <div className="App">
// //       <header className="App-header">
// //         <img src={logo} className="App-logo" alt="logo" />
// //         <p>
// //           Edit <code>src/App.js</code> and save to reload.
// //         </p>
// //         <a
// //           className="App-link"
// //           href="https://reactjs.org"
// //           target="_blank"
// //           rel="noopener noreferrer"
// //         >
// //           Learn React
// //         </a>
// //       </header>
// //     </div>
// //   );
// // }

// // export default App;
