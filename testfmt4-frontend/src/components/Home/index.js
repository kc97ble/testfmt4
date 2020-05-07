import React, { useState } from "react";
import Navbar from "react-bootstrap/Navbar";
import { Container, Row, Col, Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";

function TopBar() {
  return (
    <Navbar bg="dark" variant="dark">
      <Navbar.Brand href="#home">
        <img
          alt=""
          src="logo192.png"
          width="30"
          height="30"
          className="d-inline-block align-top"
        />{" "}
        Test Formatter 4
      </Navbar.Brand>
    </Navbar>
  );
}

function MainForm() {
  const [files, setFiles] = useState(null);

  return (
    <Form>
      <Form.File id="formcheck-api-custom" custom>
        <Form.File.Input
          files={files}
          onChange={(e) => {
            console.log(e.target.files);
            setFiles(e.target.files);
          }}
        />
        <Form.File.Label data-browse="Button text">
          {JSON.stringify(files)}
        </Form.File.Label>
      </Form.File>
      <Button variant="primary" type="submit">
        Submit
      </Button>
    </Form>
  );
}

// class MainForm extends React.Component {
//   fileChanged = (event) => {
//     console.log(event.target.files);
//     alert("fileChanged");
//   };
//   render() {

//   }
// }

export default class Home extends React.Component {
  render() {
    return (
      <div>
        <TopBar />
        <Container>
          <Row>
            <Col>
              <MainForm />
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}
