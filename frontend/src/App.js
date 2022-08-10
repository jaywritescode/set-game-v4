import { useEffect, useState } from "react";
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

const socketUrl = "ws://localhost:3001/ws";

const playerName = generate().dashed;

function App() {
  const [state, setState] = useState({
    board: [],
    players: [],
    gameState: GameStates.WAITING_TO_CONNECT,
  });

  const { sendJsonMessage, lastJsonMessage, readyState } = useWebsocket(socketUrl, {
    onOpen: () => {
      console.log("[useWebsocket:onOpen]")
    },
    onMessage: () => {
      console.log("[useWebsocket:onMessage]");
    }
  })

  useEffect(
    function messageReceived() {

      const handleIncomingMessage = (message) => {
        switch (message.action) {
          case JOIN_GAME:
            handleJoinGame(message.payload);
            break;
          case START_GAME:
            handleStartGame(message.payload);
            break;
          default:
            console.log(message.payload);
        }
      }

      const handleJoinGame = ({ success, game, error }) => {
        const gameState = R.cond([
          [R.always(game.game_over), R.always(GameStates.GAME_OVER)],
          [() => R.isEmpty(game.board), R.always(GameStates.WAITING_TO_START)],
          [R.T, R.always(GameStates.IN_PROGRESS)],
        ])();

        if (success) {
          setState({
            ...game,
            gameState,
          });
        } else {
          console.error(error);
        }
      }

      const handleStartGame = ({ success, game, error }) => {
        if (success) {
          setState({
            ...game,
            gameState: GameStates.IN_PROGRESS
          });
        } else {
          console.error(error);
        }
      }



      console.group('messageReceived');
      if (lastJsonMessage !== null) {
        console.log(lastJsonMessage);
        handleIncomingMessage(lastJsonMessage);
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
          <Board cards={state.board} />
        )}
      </main>
    </div>
  );
}

export default App;
