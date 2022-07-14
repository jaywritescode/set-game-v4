import { useEffect } from "react";
import useWebsocket, { ReadyState } from "react-use-websocket";
import generate from "project-name-generator";
import logo from './logo.svg';
import './App.css';

const JOIN_GAME = 'join_game';
const socketUrl = "ws://localhost:3001/ws";

const playerName = generate().dashed;

function App() {
  const { sendJsonMessage, readyState } = useWebsocket(socketUrl, {
    onOpen: (e) => {
      console.log('[useWebsocket:onOpen] ', e);
    },
    onMessage: (e) => {
      console.log('[useWebsocket:onMessage]', e);
    }
  });

  useEffect(function connectionEstablished() {
    if (readyState !== ReadyState.OPEN) {
      console.log("[connectionEstablished] connection is in state ", readyState);
      return;
    }

    console.log("[connectionEstablished] connection is open");
    sendJsonMessage({
      action: JOIN_GAME,
      payload: { name: playerName }
    });
  }, [readyState, sendJsonMessage]);

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
