import React from "react";

export default function Players(props) {
  const { players, myself } = props;

  return (
    <ul>
      {Object.entries(players).map(([playerName, setsFound]) => (
        <li key={playerName}>{playerName}: {setsFound.length}</li>
      ))}
    </ul>
  )
}