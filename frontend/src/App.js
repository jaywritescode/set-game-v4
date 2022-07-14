import { useEffect, useReducer } from "react";
import useWebsocket, { ReadyState } from "react-use-websocket";
import generate from "project-name-generator";
import logo from './logo.svg';
import './App.css';

const GameStates = Object.freeze({
  WAITING_TO_START: 0,
  IN_PROGRESS: 1,
  GAME_OVER: 2,
});

const JOIN_GAME = 'join_game';

const socketUrl = "ws://localhost:3001/ws";

const playerName = generate().dashed;

const reducer = (state, { action, payload }) => {
  switch (action) {
    case JOIN_GAME: {
      return handleJoinGame(state, payload)
    }
    default: {
      return state;
    }
  }
};

const handleJoinGame = (state, { success, game, error }) => {
  if (success) {
    return {
      ...state,
      board: game.board,
      players: game.players,
      game_state: getGameState(game),
    }
  }

  return state;
}

function getGameState(game) {
  if (game.game_over) {
    return GameStates.GAME_OVER;
  }
  return game.board.length ? GameStates.IN_PROGRESS : GameStates.WAITING_TO_START;
}


function App() {
  const [state, dispatch] = useReducer(reducer, {
    board: [],
    players: [],
    game_state: GameStates.WAITING_TO_START,
  });

  const { sendJsonMessage, readyState } = useWebsocket(socketUrl, {
    onOpen: (e) => {
      console.log('[useWebsocket:onOpen] ', e);
    },
    onMessage: (e) => {
      console.log('[useWebsocket:onMessage]', e);
      dispatch(JSON.parse(e.data));
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
