import React from "react";
import { Table, Button } from "react-bootstrap";
import styled from "styled-components";

const ResultsContainer = styled.div`
  margin-top: 20px;
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const ScanResults = () => {
  return (
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
  );
};

export default ScanResults;
