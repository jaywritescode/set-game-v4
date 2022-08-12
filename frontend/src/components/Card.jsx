import React from "react";
import * as R from "ramda";
import classNames from "classnames";
import styles from "./Card.module.css";

export default function Card(props) {
  const { color, number, shading, shape, onClick, selected } = props;

  const imageName = [number, color, shading, shape].map(R.toLower).join("-");

  return (
    <div
      className={classNames(styles.card, {[styles.selected]: selected})}
      style={{ backgroundImage: `url(/cards/${imageName}.png)` }}
      onClick={onClick}
    />
  );
}
