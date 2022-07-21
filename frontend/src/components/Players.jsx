import React from "react";
import styles from "./Players.module.css";

export default function Players(props) {
  const { players, myself } = props;

  return (
    <div className={styles.container}>
      <h2 className={styles.header}>Players</h2>
      <div className={styles.playerList}>
        {Object.entries(players).map(([playerName, setsFound]) => (
          <li key={playerName}>{playerName}: {setsFound.length}</li>
        ))}
      </div>
    </div>
  )
}