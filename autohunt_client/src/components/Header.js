import React from "react";
import { Navbar, Container, Nav } from "react-bootstrap";

const Header = () => (
  <Navbar bg="dark" variant="dark" expand="lg">
    <Container>
      <Navbar.Brand href="#home">AutoHunt</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="me-auto">
          <Nav.Link href="#home">Home</Nav.Link>
          <Nav.Link href="#scans">Scans</Nav.Link>
          <Nav.Link href="#results">Results</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default Header;
