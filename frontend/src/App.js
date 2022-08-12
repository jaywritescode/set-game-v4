import { useEffect, useReducer } from "react";
import useWebsocket, { ReadyState } from "react-use-websocket";
import generate from "project-name-generator";
import * as R from "ramda";
import "./App.css";
import Players from "./components/Players";
import Board from "./components/Board";

const GameStates = Object.freeze({
  WAITING_TO_CONNECT: 0,
  WAITING_TO_START: 1,
  IN_PROGRESS: 2,
  GAME_OVER: 3,
});

const JOIN_GAME = "join_game";
const START_GAME = "start_game";
const SELECT_CARD = "selectCard";
const DESELECT_CARD = "deselectCard";

const socketUrl = "ws://localhost:3001/ws";

const playerName = generate().dashed;

function reducer(state, {action, payload}) {
  switch (action) {
    case JOIN_GAME:
      return {...state, ...handleJoinGame(payload) };
    case START_GAME:
      return {...state, ...handleStartGame(payload)};
    case SELECT_CARD:
      return {...state, selected: [...state.selected, payload]}
    case DESELECT_CARD:
      return {...state, selected: R.without([payload], state.selected)}
    default:
      throw new Error();
  }
}

function handleJoinGame({ success, game, error }) {
  const gameState = R.cond([
    [R.always(game.game_over), R.always(GameStates.GAME_OVER)],
    [() => R.isEmpty(game.board), R.always(GameStates.WAITING_TO_START)],
    [R.T, R.always(GameStates.IN_PROGRESS)],
  ])();

  if (error) {
    console.log(error);
  }

  return {...game, gameState};
}

function handleStartGame({ success, game, error }) {
  if (success) {
    return {...game, gameState: GameStates.IN_PROGRESS}
  } else {
    console.error(error);
    return {gameState: GameStates.IN_PROGRESS};
  }
}

function App() {
  const [state, dispatch] = useReducer(reducer, {
    board: [],
    players: [],
    selected: [],
    gameState: GameStates.WAITING_TO_CONNECT,
  })

  const { sendJsonMessage, lastJsonMessage, readyState } = useWebsocket(
    socketUrl,
    {
      onOpen: () => {
        console.log("[useWebsocket:onOpen]");
      },
      onMessage: () => {
        console.log("[useWebsocket:onMessage]");
      },
    }
  );

  useEffect(
    function messageReceived() {
      console.group("messageReceived");
      if (lastJsonMessage !== null) {
        console.log(lastJsonMessage);
        dispatch(lastJsonMessage);
      }
      console.groupEnd();
    },
    [lastJsonMessage]
  );

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

  const onClickStartGame = () => {
    sendJsonMessage({
      action: START_GAME,
      payload: {},
    });
  };

  return (
    <div className="App">
      <main className="App-main">
        <Players players={state.players} myself={playerName} />

        {state.gameState === GameStates.WAITING_TO_START && (
          <button onClick={onClickStartGame}>start game</button>
        )}
        {state.gameState === GameStates.IN_PROGRESS && (
          <Board cards={state.board} selected={state.selected} dispatch={dispatch} />
        )}
      </main>
    </div>
  );
}

export default App;
