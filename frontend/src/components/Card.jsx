import React from "react";
import * as R from "ramda";

export default function Card(props) {
  const { color, number, shading, shape } = props;

  const imageName = [number, color, shading, shape].map(R.toLower).join("-");

  return <div style={{ backgroundImage: `url(/cards/${imageName}.png)` }} />;
}
