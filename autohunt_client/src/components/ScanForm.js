import React, { useState } from 'react';
import { Form, Button } from "react-bootstrap";
import styled from "styled-components";

const FormContainer = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
`;

const ScanForm = () => {
  // 1. Set up local state for the form fields
  const [scanName, setScanName] = useState('');
  const [targetIP, setTargetIP] = useState('');

  // 2. Handler when form is submitted
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("hello");
    
    try {
      const response = await fetch('/api/scans', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scanName,
          target: targetIP,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        console.log('Scan started:', data);
        // handle success, e.g. show user a success message
      } else {
        console.error('Error:', data);
        // handle error, show user an error message
      }
    } catch (err) {
      console.error('Request failed:', err);
    }
  };

  return (
    <FormContainer>
      <h3>Start a New Scan</h3>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formScanName">
          <Form.Label>Scan Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter scan name"
            value={scanName}
            onChange={(e) => setScanName(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formTargetIP">
          <Form.Label>Target IP</Form.Label>
          <Form.Control
            type="text"
            value={targetIP}
            onChange={e => setTargetIP(e.target.value.trim())}
          />

        </Form.Group>

        <Button variant="primary" type="submit">
          Start Scan
        </Button>
      </Form>
    </FormContainer>
  );
};

export default ScanForm;