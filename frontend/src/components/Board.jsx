import { splitEvery, toLower } from "ramda";
import React from "react";
import Card from "./Card";


export default function Board(props) {
  const { cards } = props;

  return (
    <>
      {splitEvery(3, cards).map((triplet, index) => (
        <div key={index}>
          {triplet.map((card) => (
            <div key={card}>
              <Card {...card} />
            </div>
          ))}
        </div>
      ))}
    </>
  );
}
