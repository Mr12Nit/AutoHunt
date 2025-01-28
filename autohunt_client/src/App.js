import React from "react";
import { Container, Navbar, Form, Button, Table } from "react-bootstrap";
import styled from "styled-components";

const HeaderContainer = styled.div`
  background-color: #007bff;
  padding: 10px;
  color: white;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
`;

const FormContainer = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
`;

const ResultsContainer = styled.div`
  margin-top: 20px;
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const App = () => {
  return (
    <Container>
      <HeaderContainer>
        AutoHunt Client
      </HeaderContainer>

      <FormContainer>
        <h3>Start a New Scan</h3>
        <Form>
          <Form.Group className="mb-3" controlId="formScanName">
            <Form.Label>Scan Name</Form.Label>
            <Form.Control type="text" placeholder="Enter scan name" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formTargetURL">
            <Form.Label>Target URL</Form.Label>
            <Form.Control type="url" placeholder="https://example.com" />
          </Form.Group>

          <Button variant="primary" type="submit">
            Start Scan
          </Button>
        </Form>
      </FormContainer>

      <ResultsContainer>
        <h3>Scan Results</h3>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>#</th>
              <th>Scan Name</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Example Scan</td>
              <td>Completed</td>
              <td>
                <Button variant="info" size="sm">View</Button>
                <Button variant="danger" size="sm" className="ms-2">Delete</Button>
              </td>
            </tr>
          </tbody>
        </Table>
      </ResultsContainer>
    </Container>
  );
};

export default App;
