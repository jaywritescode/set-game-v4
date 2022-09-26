import React, { useState } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Stack from 'react-bootstrap/Stack';

export default function PlayerNameForm(props) {

  const { onClickJoinGame } = props;

  const [name, setName] = useState('');

  return (
    <Stack direction="horizontal" gap={3}>
      <Form.Control 
        type="text" 
        placeholder="Your name..."
        onChange={(e) => setName(e.currentTarget.value)} />
      <Button variant="primary" onClick={() => onClickJoinGame(name)}>Join Game</Button>
    </Stack>
  );
}