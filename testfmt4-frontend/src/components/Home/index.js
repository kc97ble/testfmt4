import React, { useState } from "react";

import { Container, Row, Col, Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import { useHistory } from "react-router-dom";
import * as api from "../../api";
import TopBar from "../../common/TopBar";
import "./style.css";

function get(obj, ...args) {
  for (let i = 0; i < args.length; i++) {
    if (obj == null) {
      return null;
    }
    obj = obj[args[i]];
  }
  return obj;
}

function MainForm() {
  const [files, setFiles] = useState(null);
  const [loading, setLoading] = useState(false);

  const history = useHistory();
  const fileName = get(files, 0, "name");
  const caption = loading ? "Uploading..." : "Upload";

  return (
    <Form>
      <Form.File custom>
        <Form.File.Input
          files={files}
          onChange={(e) => {
            console.log(e.target.files);
            setFiles(e.target.files);
          }}
          disabled={loading}
        />
        <Form.File.Label data-browse="Choose file">{fileName || ""}</Form.File.Label>
      </Form.File>
      <Button
        variant="primary"
        className="mt-3"
        block={true}
        disabled={!fileName || loading}
        onClick={async () => {
          setLoading(true);
          const { file_id: fileID } = await api.uploadFile({ file: files[0] });
          setLoading(false);
          history.push("/edit/" + fileID);
        }}
      >
        {caption}
      </Button>
    </Form>
  );
}

function Banner() {
  return (
    <div className="banner">
      <h3 style={{ textAlign: "center" }}>Format your test suite</h3>
    </div>
  );
}

export default function Home() {
  return (
    <div>
      <TopBar />
      <Container
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          height: "calc(80vh - 100px)",
          minHeight: "300px",
        }}
      >
        <Row>
          <Col>
            <Banner />
            <MainForm />
          </Col>
        </Row>
      </Container>
    </div>
  );
}
