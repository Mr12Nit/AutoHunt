import React from "react";
import styled from "styled-components";

const HeaderContainer = styled.div`
  background-color: #007bff;
  padding: 10px;
  color: white;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
`;

const Header = () => {
  return <HeaderContainer>AutoHunt Client</HeaderContainer>;
};

export default Header;
