import React from "react";
import { Container } from "react-bootstrap";
import { AppContainer, Footer } from "./styles/AppStyles";
import Header from "./components/Header";
import ScanForm from "./components/ScanForm";
import ScanResults from "./components/ScanResults";

const App = () => {
  const [results, setResults] = React.useState([]);

  const handleScanSubmit = (event) => {
    event.preventDefault();
    setResults([
      { target: "192.168.1.1", status: "Complete", details: "No issues found." },
      { target: "example.com", status: "Complete", details: "Vulnerabilities detected." },
    ]);
  };

  return (
    <AppContainer>
      <Header />
      <Container>
        <h1 className="my-4">Initiate a Scan</h1>
        <ScanForm onSubmit={handleScanSubmit} />
        <h2 className="my-4">Scan Results</h2>
        <ScanResults results={results} />
      </Container>
      <Footer>
        <p>&copy; {new Date().getFullYear()} AutoHunt</p>
      </Footer>
    </AppContainer>
  );
};

export default App;
