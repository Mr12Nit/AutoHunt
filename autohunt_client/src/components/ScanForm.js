import React from "react";
import { Row, Col, Button, Form } from "react-bootstrap";

const ScanForm = ({ onSubmit }) => (
  <Form onSubmit={onSubmit}>
    <Row className="mb-3">
      <Col>
        <Form.Control placeholder="Target URL or IP" />
      </Col>
      <Col>
        <Button variant="primary" type="submit">
          Start Scan
        </Button>
      </Col>
    </Row>
  </Form>
);

export default ScanForm;
