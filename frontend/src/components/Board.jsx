import React from "react";
import Card from "./Card";
import styles from "./Board.module.css";

export default function Board(props) {
  const { cards } = props;

  return (
    <div className={styles.container}>
      {cards.map(card => (<Card {...card} />))}
    </div>
  );
}
