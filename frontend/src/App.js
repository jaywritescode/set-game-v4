import { useReducer } from "react";
import useWebsocket, { ReadyState } from "react-use-websocket";
import logo from './logo.svg';
import './App.css';
import WaitingToStart from "./components/WaitingToStart";

const socketUrl = "ws://localhost:3001/ws";

function App() {
  const { sendJsonMessage, readyState } = useWebsocket(socketUrl, {
    onOpen: (e) => {
      console.log('[useWebsocket:onOpen] ', e);
    },
    onMessage: (e) => {
      console.log('[useWebsocket:onMessage]', e);
    }
  });

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
