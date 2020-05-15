import React from "react";
import Navbar from "react-bootstrap/Navbar";

export default function TopBar() {
  return (
    <Navbar bg="dark" variant="dark">
      <Navbar.Brand href="/">
        <img alt="" src="/logo192.png" width="30" height="30" className="d-inline-block align-top mr-2" />
        Test Formatter 4
      </Navbar.Brand>
    </Navbar>
  );
}
