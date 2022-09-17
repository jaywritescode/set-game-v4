import { useEffect, useReducer } from "react";
import useWebsocket, { ReadyState } from "react-use-websocket";
import generate from "project-name-generator";
import * as R from "ramda";
import Button from "react-bootstrap/Button";


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
const SUBMIT = "submit";

const socketUrl = "ws://localhost:3001/ws";

const playerName = generate().dashed;

function reducer(state, { action, payload }) {
  switch (action) {
    case JOIN_GAME:
      return { ...state, ...handleJoinGame(payload) };
    case START_GAME:
      return { ...state, ...handleStartGame(payload) };
    case SUBMIT:
      return { ...state, ...handleSubmit(state, payload) };
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

  return { ...game, gameState };
}

function handleStartGame({ success, game, error }) {
  if (success) {
    return { ...game, gameState: GameStates.IN_PROGRESS };
  } else {
    console.error(error);
    return { gameState: GameStates.IN_PROGRESS };
  }
}

function handleSubmit(state, { success, game, error }) {
  function updateBoard() {
    const cardsToRemove = R.difference(state.board, game.board);
    const cardsToAdd = R.difference(game.board, state.board);

    return R.concat(
      state.board.map((card) =>
        cardsToRemove.find(R.equals(card)) ? cardsToAdd.shift() : card
      ),
      cardsToAdd
    );
  }

  if (success) {
    return {
      players: game.players,
      board: updateBoard(),
    };
  } else {
    return {};
  }
}

const getSubmitMessage = (cards) => {
  return {
    action: SUBMIT,
    payload: {
      player: playerName,
      cards,
    },
  };
};

function App() {
  const [state, dispatch] = useReducer(reducer, {
    board: [],
    players: [],
    gameState: GameStates.WAITING_TO_CONNECT,
  });

  const { sendJsonMessage, lastJsonMessage, readyState } = useWebsocket(
    socketUrl,
    {
      onOpen: () => {
        console.log("[App:useWebsocket:onOpen]");
      },
      onMessage: () => {
        console.log("[App:useWebsocket:onMessage]");
      },
      share: true,
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
          <Button onClick={onClickStartGame}>start game</Button>
        )}
        {state.gameState === GameStates.IN_PROGRESS && (
          <Board
            cards={state.board}
            submit={getSubmitMessage}
            lastMessage={lastJsonMessage}
          />
        )}
      </main>
    </div>
  );
}

export default App;
