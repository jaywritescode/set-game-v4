import React, { useState } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

export default function PlayerNameForm(props) {

  const { onClickJoinGame } = props;

  const [name, setName] = useState('');

  return (
    <Form>
      <Form.Group className="mb-3" controlId="playerName">
        <Form.Label>Your Name</Form.Label>
        <Form.Control type="text" onChange={(e) => setName(e.currentTarget.value)}/>
        <Button variant="primary" onClick={() => onClickJoinGame(name)}>Join Game</Button>
      </Form.Group>
    </Form>
  );
}