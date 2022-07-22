import { useEffect, useReducer } from "react";
import useWebsocket, { ReadyState } from "react-use-websocket";
import generate from "project-name-generator";
import * as R from "ramda";
import logo from "./logo.svg";
import "./App.css";
import Players from "./components/Players";
import WaitingToStart from "./components/WaitingToStart";

const GameStates = Object.freeze({
  WAITING_TO_START: 0,
  IN_PROGRESS: 1,
  GAME_OVER: 2,
});

const JOIN_GAME = "join_game";
const START_GAME = "start_game";

const socketUrl = "ws://localhost:3001/ws";

const playerName = generate().dashed;

const reducer = (state, { action, payload }) => {
  switch (action) {
    case JOIN_GAME: {
      return handleJoinGame(state, payload);
    }
    default: {
      return state;
    }
  }
};

const handleJoinGame = (state, { success, game, error }) => {
  if (success) {
    return Object.assign(
      { ...state },
      {
        board: game.board,
        players: game.players,
      },
      {
        gameState: R.cond([
          [R.always(game.game_over), R.always(GameStates.GAME_OVER)],
          [() => R.isEmpty(game.board), R.always(GameStates.WAITING_TO_START)],
          [R.T, R.always(GameStates.IN_PROGRESS)],
        ])(),
      }
    );
  }

  return state;
};

function App() {
  const [state, dispatch] = useReducer(reducer, {
    board: [],
    players: [],
    gameState: GameStates.WAITING_TO_START,
  });

  const { sendJsonMessage, readyState } = useWebsocket(socketUrl, {
    onOpen: (e) => {
      console.log("[useWebsocket:onOpen] ", e);
    },
    onMessage: (e) => {
      console.log("[useWebsocket:onMessage]", e);
      dispatch(JSON.parse(e.data));
    },
  });

  useEffect(
    function connectionEstablished() {
      if (readyState !== ReadyState.OPEN) {
        console.log(
          "[connectionEstablished] connection is in state ",
          readyState
        );
        return;
      }

      console.log("[connectionEstablished] connection is open");
      sendJsonMessage({
        action: JOIN_GAME,
        payload: { name: playerName },
      });
    },
    [readyState, sendJsonMessage]
  );

  return (
    <div className="App">
      <main className="App-main">
        <Players players={state.players} myself={playerName} />
      </main>
    </div>
  );
}

export default App;
