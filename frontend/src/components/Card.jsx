import React from "react";
import * as R from "ramda";
import styles from "./Card.module.css";

export default function Card(props) {
  const { color, number, shading, shape, onClick } = props;

  const imageName = [number, color, shading, shape].map(R.toLower).join("-");

  return (
    <div
      className={styles.card}
      style={{ backgroundImage: `url(/cards/${imageName}.png)` }}
      onClick={onClick}
    />
  );
}
