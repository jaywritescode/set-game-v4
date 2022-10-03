import { useEffect, useReducer } from "react";
import useWebsocket, { ReadyState } from "react-use-websocket";
import * as R from "ramda";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";

import "./App.css";
import Players from "./components/Players";
import Board from "./components/Board";
import PlayerNameForm from "./components/PlayerNameForm";

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

function reducer(state, { action, payload }) {
  switch (action) {
    case 'connect':
      return { ...state, isConnected: true };
    case 'disconnect':
      return { ...state, isConnected: false };
    case 'set_name':
      return { ...state, playerName: payload.name };
    case 'fetch_game':
      return { ...state, ...handleFetchGame(payload) };
    case JOIN_GAME:
      return { ...state, ...handleJoinGame(state, payload) };
    case START_GAME:
      return { ...state, ...handleStartGame(payload) };
    case SUBMIT:
      return { ...state, ...handleSubmit(state, payload) };
    default:
      throw new Error();
  }
}

function handleFetchGame({ success, game, error }) {
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

function handleJoinGame(state, { success, name, players, error }) {
  if (error) {
    console.log(error);
  }

  const isJoined = success && name === state.playerName;

  return { players, isJoined };
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

const getSubmitMessage = (player, cards) => {
  return {
    action: SUBMIT,
    payload: {
      player,
      cards,
    },
  };
};

function App() {
  const [state, dispatch] = useReducer(reducer, {
    isConnected: false,
    isJoined: false,
    board: [],
    players: [],
    playerName: null,
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
        dispatch({ action: 'disconnect' });
        return;
      }

      console.log("[connectionEstablished] connection is open");
      dispatch({ action: 'connect' })
      sendJsonMessage({
        action: 'fetch_game',
        payload: { },
      });
    },
    [readyState, sendJsonMessage]
  );

  const onClickJoinGame = (name) => {
    dispatch({ action: 'set_name', payload: {
      name
    }});
    sendJsonMessage({
      action: JOIN_GAME,
      payload: {
        name
      }
    });
  }

  const onClickStartGame = () => {
    sendJsonMessage({
      action: START_GAME,
      payload: {},
    });
  };

  return (
    <div className="App">
      <main className="App-main">
        <Container>
          <Row xs={1} md={2}>
            <Col>
              {!state.playerName && <PlayerNameForm onClickJoinGame={onClickJoinGame} />}
              
              <Players players={state.players} myself={state.playerName} />
            </Col>
            <Col>
              {state.isJoined && state.gameState === GameStates.WAITING_TO_START && (
                          <Button onClick={onClickStartGame}>start game</Button>
              )}
              {state.gameState === GameStates.IN_PROGRESS && (
                <Board
                  cards={state.board}
                  isJoined={state.isJoined}
                  submit={R.partial(getSubmitMessage, [state.playerName])}
                  lastMessage={lastJsonMessage}
                />
              )}    
            </Col>
          </Row>
        </Container>
        
      </main>
    </div>
  );
}

export default App;
