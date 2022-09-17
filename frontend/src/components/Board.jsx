import React, { useEffect, useState } from "react";
import useWebsocket from "react-use-websocket";
import Card from "./Card";
import styles from "./Board.module.css";
import * as R from "ramda";

const socketUrl = "ws://localhost:3001/ws";

export default function Board(props) {
  const { cards, lastMessage, submit } = props;

  const [selected, setSelected] = useState([]);

  const { sendJsonMessage } = useWebsocket(socketUrl, {
    onOpen: () => {
      console.log("[Board:useWebsocket:onOpen]");
    },
    onMessage: () => {
      console.log("[Board:useWebsocket:onMessage]");
    },
    share: true,
  });

  const onCardClicked = (card) => {
    console.log("onCardClicked: ", card);

    if (selected.find(R.equals(card))) {
      setSelected(R.without([card], selected));
    } else if (selected.length < 3) {
      setSelected([...selected, card]);
    }
  };

  useEffect(
    function doSubmit() {
      if (selected.length === 3) {
        sendJsonMessage(submit(selected));
      }
    },
    [submit, selected, sendJsonMessage]
  );

  useEffect(
    function resetSelected() {
      if (lastMessage?.action === "submit" && lastMessage?.payload.success) {
        setSelected([]);
      }
    },
    [lastMessage]
  );

  return (
    <div className={styles.container}>
      {cards.map((card) => (
        <Card
          {...card}
          onClick={() => onCardClicked(card)}
          key={`${card.number}-${card.color}-${card.shading}-${card.shape}`}
          selected={selected.find(R.equals(card)) !== undefined}
        />
      ))}
    </div>
  );
}
