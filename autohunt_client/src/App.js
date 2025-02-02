import React from "react";
import { Container } from "react-bootstrap";
import Header from "./components/Header";
import ScanForm from "./components/ScanForm";
import ScanResults from "./components/ScanResults";

const App = () => {
  return (
    <Container>
      <Header />
      <ScanForm />
      <ScanResults />
    </Container>
  );
};

export default App;