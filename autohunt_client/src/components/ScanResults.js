import React from "react";
import { Table } from "react-bootstrap";

const ScanResults = ({ results }) => (
  <Table striped bordered hover>
    <thead>
      <tr>
        <th>#</th>
        <th>Target</th>
        <th>Status</th>
        <th>Details</th>
      </tr>
    </thead>
    <tbody>
      {results.length > 0 ? (
        results.map((result, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{result.target}</td>
            <td>{result.status}</td>
            <td>{result.details}</td>
          </tr>
        ))
      ) : (
        <tr>
          <td colSpan="4">No results available</td>
        </tr>
      )}
    </tbody>
  </Table>
);

export default ScanResults;
