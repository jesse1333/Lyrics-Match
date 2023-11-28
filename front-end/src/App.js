import React, {useState} from 'react';
import './App.css'; // Import your CSS file
import logo from './assets/microphone.svg'

function App() {
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
  
  const SearchBar = (left) => {
    const [data, setData] = useState()

    const inputStyle= { position: 'absolute', 
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)'
    }

    const handleKeyDown = (event) => {
      if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default Enter key behavior (e.g., form submission)
        document.getElementById("lyrics-input").value = ""; // Clear the input value


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

  const Square = ({left, right, flex}) => {
    const squareStyle = {
      left: left,
      right: right,
      top: '55%',
      flex: flex,
    };

    return (
      <div className="square" style={squareStyle}>     
      </div>
    );
  };
  
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
      <div className="albumns-container">
      <Square></Square>
      <Square></Square>
      <Square></Square>

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
