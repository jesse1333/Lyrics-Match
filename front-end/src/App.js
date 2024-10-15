import React, { useState } from 'react';
import './App.css'; // Import your CSS file
import logo from './assets/microphone.svg';

function App() {
  const OrangeBorder = {
    top: '0',
    left: '0',
    width: '100%',
    height: '40vh',
    backgroundColor: 'orange',
    position: 'absolute',
    marginTop: '0',
    zIndex: '-1',
  };

  const SearchBar = () => {
    const [data, setData] = useState('');
    const [results, setResults] = useState([]); // State to hold search results

    const inputStyle = {
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
    };

    const handleKeyDown = async (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();

        const response = await fetch('http://127.0.0.1:5000/search', { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: data }),
        });
        
        if (response.ok) {
          const results = await response.json();
          setResults(results); // Update state with the fetched results
        } else {
          console.error('Error fetching results');
        }

        setData(''); // Clear input value
      }
    };

    const handleChange = (event) => {
      setData(event.target.value);
    };

    return (
      <div className="form__group field" style={inputStyle}>
        <input
          type="input"
          value={data}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          className="form__field"
          placeholder="lyrics"
          name="lyrics-input"
          id="lyrics-input"
          required
        />
        <label htmlFor="lyrics-input" className="form__label">Lyrics:</label>
        <h1>{data}</h1>

        {/* Display the results */}
        {/* <div>
          {results.map((result, index) => (
            <div key={index}>
              <h2>{result.title}</h2>
              <p>Similarity Score: {result.similarity_score}</p>
            </div>
          ))}
        </div> */}
      </div>
    );
  };

  const Square = ({ left, right, flex }) => {
    const squareStyle = {
      left: left,
      right: right,
      top: '55%',
      flex: flex,
    };

    return <div className="square" style={squareStyle}></div>;
  };

  return (
    <div className="App">
      <div className="orange-border" style={{ ...OrangeBorder }}></div>

      <div className="title-container" style={{ position: 'absolute' }}>
        <h1 style={{ position: 'relative', fontSize: 40, left: 30 }}>Lyrics Match</h1>
        <img src={logo} alt="Microphone Logo" style={{ height: 40, width: 40, position: 'relative', left: 190, top: -70 }} />
      </div>

      <div className="search-bar-container">
        <SearchBar />
      </div>
      <div className="albumns-container">
        <Square />
        <Square />
        <Square />
      </div>
    </div>
  );
}

export default App;
