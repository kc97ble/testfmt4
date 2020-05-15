import React from "react";
import { useParams } from "react-router-dom";
import TopBar from "../../common/TopBar";
import { Container, Row, Col } from "react-bootstrap";
import * as api from "../../api";

import "../../common/sharedStyles.css";
import { Button } from "react-bootstrap";

export default function Download(props) {
  const { fileID } = useParams();
  return (
    <div>
      <TopBar />
      <Container className="container">
        <Row>
          <Col>
            <h1>Download your test suite</h1>
            <p>Your test suite has been formatted!</p>
            <Button onClick={() => api.downloadFile(fileID)}>Download</Button>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
