import './App.css';
import Navbar from './NavBar';
import Home from './Home';
function App() {
  const like = 50;
  return (
    <div className="App">
      <Navbar/>
      <div className="conent">
        <Home />
      </div>
    </div>
  );
}

export default App;
