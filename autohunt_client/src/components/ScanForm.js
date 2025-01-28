import React from "react";
import { Row, Col, Button, Form, Card } from "react-bootstrap";

const ScanForm = ({ onSubmit }) => (
  <Card className="shadow-sm">
    <Card.Body>
      <Form onSubmit={onSubmit}>
        <Row>
          <Col xs={12} className="mb-3">
            <Form.Control
              type="text"
              placeholder="Enter Target URL or IP"
              className="p-3"
            />
          </Col>
          <Col xs={12}>
            <Button type="submit" variant="primary" className="w-100 py-2">
              Start Scan
            </Button>
          </Col>
        </Row>
      </Form>
    </Card.Body>
  </Card>
);

export default ScanForm;
