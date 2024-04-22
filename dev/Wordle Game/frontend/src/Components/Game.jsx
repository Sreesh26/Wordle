import { useState, useEffect } from 'react';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';

function Game() {
    const [guesses, setGuesses] = useState(Array(6).fill(Array(5).fill('')));
    const [currentGuess, setCurrentGuess] = useState(0);
    const [results, setResults] = useState([]);
    const [tokenPresent, setTokenPresent] = useState(false);
    const navigate = useNavigate();


    useEffect(() => {
      const token = localStorage.getItem('token');

      if (!token) {
          // Redirect to login if token is not present
          console.log("inside if")
          console.error("No token found")
          return;
      }

      else {
        setTokenPresent(true);
        console.log("inside else")
        fetchGameData(token);
      }
      // Fetch game data using token for authentication
      async function fetchGameData(token) {
          try {
              const response = await axios.post('http://localhost:5000/guess', {
                  guess: 'example_guess',  // Replace with actual game data
              }, {
                  headers: {
                      Authorization: `Bearer ${token}`
                  }
              });

              setResults(response.data);
          } catch (error) {
              console.error('Error fetching game data:', error);
          }
      }

    }, []);
  
    const updateGuess = (guessIndex, charIndex, char) => {
      const newGuesses = guesses.slice();
      const newGuess = [...newGuesses[guessIndex]];
      newGuess[charIndex] = char.toUpperCase();
      newGuesses[guessIndex] = newGuess;
      setGuesses(newGuesses);
    };

    const handleLogout = () => {
      // Clear token from localStorage
      localStorage.removeItem('token');
      // Redirect to login page
      window.location.href = '/';
    };
  
    const handleSubmit = async () => {
        console.log(guesses)
        console.log(currentGuess)
        if (currentGuess >= 6) return; // Prevent more than 6 guesses
        try {
          const response = await axios.post('http://localhost:5000/guess', {
            guess: guesses[currentGuess].join(''),
          });
          
          console.log(response)
          setResults([...results, response.data]);
          console.log(results)
          setCurrentGuess(currentGuess + 1);
        } catch (error) {
          console.error('Error submitting guess:', error);
        }
      };
  
    const getColorClass = (result) => {
        console.log(result)
      switch (result) {
        case 'correct':
          return 'bg-green-500 border-green-500 text-white';
        case 'present':
          return 'bg-yellow-500 border-yellow-500 text-white';
        case 'absent':
            return 'bg-gray-600 border-gray-600 text-white';
        default:
          return 'bg-green-500 border-gray-500 text-white';
      }
    };
  
    return (
      <div className="flex flex-col items-center p-4">
        <button
        onClick={handleLogout}
        className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
        Logout
      </button>
        <div className="grid grid-cols-5 gap-2 mb-4 mt-16">
          {guesses.map((guess, guessIndex) =>
            guess.map((char, charIndex) => (
              <input
                key={`${guessIndex}-${charIndex}`}
                className={`w-14 h-14 text-2xl text-center uppercase border-2 ${
                  results[guessIndex] ? getColorClass(results[guessIndex][charIndex]) : 'border-gray-300'
                }`}
                maxLength="1"
                value={char}
                onChange={(e) => updateGuess(guessIndex, charIndex, e.target.value)}
                disabled={guessIndex !== currentGuess}
              />
            ))
          )}
        </div>
        <button
          onClick={handleSubmit}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-green-300"
          disabled={currentGuess >= 6}
        >
         Submit
        </button> 
        <button onClick={() => navigate('/hints')} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
              Show Hints
        </button>
      </div>
    );
}

export default Game;
