import React from "react";
import Card from "./Card";
import styles from "./Board.module.css";
import * as R from "ramda";

export default function Board(props) {
  
  const { cards, selected, dispatch } = props;

  const onCardClicked = (card) => {
    console.log("onCardClicked: ", card);

    const action = selected.find(R.equals(card)) ? "deselectCard" : "selectCard";
    dispatch({ action, payload: card });
  };

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
