import { splitEvery } from "ramda";
import React from "react";
import Card from "./Card";

export default function Board(props) {
  const { cards } = props;

  return (
    <>
      {splitEvery(3, cards).map(triplet => (
        <ul>
          {triplet.map(card => (<li>
            <Card {...card} />
          </li>))}
        </ul>
      ))}
    </>
  )
}