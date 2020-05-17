import React, { useEffect, useState } from "react";
import { useParams, useHistory } from "react-router-dom";
import TopBar from "../../common/TopBar";
import { Container, Row, Col } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import * as api from "../../api";

import "../../common/sharedStyles.css";
import { Button } from "react-bootstrap";

async function previewFile(fileID) {
  const data = await api.previewFile(fileID);
  return {
    fileName: data.file_name,
    fileSize: data.file_size,
    content: data.content,
  };
}

function get(obj, ...args) {
  for (let i = 0; i < args.length; i++) {
    if (obj == null) {
      return null;
    }
    obj = obj[args[i]];
  }
  return obj;
}

export default function Download(props) {
  const history = useHistory();
  const { fileID } = useParams();
  const [state, setState] = useState({});

  useEffect(() => {
    (async () => {
      const data = await previewFile(fileID);
      setState(data);
    })();
  }, [fileID]);

  const names = get(state, "content") || [];

  return (
    <div>
      <TopBar />
      <Container className="container">
        <Row>
          <Col>
            <h1>Download your test suite</h1>
            <p>Your test suite has been formatted!</p>
            <p>
              <strong>{get(state, "fileName") || "Loading..."}</strong> ({get(state, "fileSize") || "..."} bytes)
            </p>
          </Col>
        </Row>
        <Row>
          <Col>
            <Form.Control rows="10" as="textarea" value={names.join("\n")} readOnly />
          </Col>
        </Row>
        <Row className="mt-3">
          <Col>
            <Button className="mr-2" onClick={() => api.downloadFile(fileID)}>
              Download
            </Button>
            <Button className="mr-2" onClick={() => history.push(`/edit/${fileID}`)} variant="secondary">
              Edit
            </Button>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
