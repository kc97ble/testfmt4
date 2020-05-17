import React from "react";
import TopBar from "../../common/TopBar";
import { Container, Row, Col } from "react-bootstrap";
import { helpContent } from "./helpContent";

export default function Help() {
  return (
    <div>
      <TopBar />
      <Container>
        <Row>
          <Col>
            <pre style={{ whiteSpace: "pre-wrap" }}>{helpContent}</pre>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
