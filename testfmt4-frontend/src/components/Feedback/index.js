import React from "react";
import TopBar from "../../common/TopBar";
import { Container, Row, Col } from "react-bootstrap";

export default function Feedback() {
  return (
    <div>
      <TopBar />
      <Container>
        <Row>
          <Col>
            <iframe
              src="https://minnit.chat/testfmt4?embed&nickname="
              style={{ border: "none", width: "90%", height: "500px" }}
              allowTransparency="true"
            ></iframe>
            <br />
            <a href="https://minnit.chat/testfmt4" target="_blank">
              Free HTML5 Chatroom powered by Minnit Chat
            </a>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
