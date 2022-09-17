import React from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

export default function PlayerNameForm(props) {
  return (
    <Form>
      <Form.Group className="mb-3" controlId="playerName">
        <Form.Label>Your Name</Form.Label>
        <Form.Control type="text" />
        <Button variant="primary" type="submit">Join Game</Button>
      </Form.Group>
    </Form>
  );
}