import React from "react";
import { Table, Card } from "react-bootstrap";

const ScanResults = ({ results }) => (
  <Card className="shadow-sm">
    <Card.Body>
      <Table bordered hover responsive className="mb-0">
        <thead className="table-dark">
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
              <td colSpan="4" className="text-center text-muted">
                No results available
              </td>
            </tr>
          )}
        </tbody>
      </Table>
    </Card.Body>
  </Card>
);

export default ScanResults;
