import React, { useReducer } from "react";
import Card from "./Card";
import styles from "./Board.module.css";
import * as R from "ramda";

function reducer(state, action) {
  switch (action.type) {
    case "deselectCard":
      return R.without([action.payload], state);
    case "selectCard":
      return [...state, action.payload];
    default:
      throw new Error();
  }
}

export default function Board(props) {
  const [state, dispatch] = useReducer(reducer, []);

  const { cards } = props;

  const onCardClicked = (card) => {
    console.log("onCardClicked: ", card);

    const type = state.find(R.equals(card)) ? "deselectCard" : "selectCard";
    dispatch({ type, payload: card });
  };

  return (
    <div className={styles.container}>
      {cards.map((card) => (
        <Card
          {...card}
          onClick={() => onCardClicked(card)}
          key={`${card.number}-${card.color}-${card.shading}-${card.shape}`}
          selected={state.find(R.equals(card)) !== undefined}
        />
      ))}
    </div>
  );
}
