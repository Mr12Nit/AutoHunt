import React from "react";
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
  return (
    <FormContainer>
      <h3>Start a New Scan</h3>
      <Form>
        <Form.Group className="mb-3" controlId="formScanName">
          <Form.Label>Scan Name</Form.Label>
          <Form.Control type="text" placeholder="Enter scan name" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formTargetIP">
          <Form.Label>Target IP</Form.Label>
          <Form.Control 
            type="text" 
            placeholder="192.168.1.1" 
            pattern="^(?:\d{1,3}\.){3}\d{1,3}$"
            title="Enter a valid IP address (e.g., 192.168.1.1)" 
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
