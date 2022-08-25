
import './App.css';
import { Route, Routes } from 'react-router';
import Begin from "../src/components/begin"
import Navbar from './components/navbar';
import Configure from './components/configure';
import Room from './components/room';
import { io } from 'socket.io-client';

function App() {

  //estabelece conexão com o socket
  const socket = io.connect("http://https://evideos.herokuapp.com/");
  
  return (



    <div className="App">
      <Navbar />
      <main className="App-body">
        <Routes>
          <Route path="/" element={<Begin />} />
          <Route path="/entrar" element={<Configure socket={socket} />} />
          <Route path="/room" element={<Room socket={socket} />} />


        </Routes>

      </main>
    </div>
  );
}

export default App;
