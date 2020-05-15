import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useHistory, useParams } from "react-router-dom";
import * as api from "../../api";
import TopBar from "../../common/TopBar";
import "../../common/sharedStyles.css";

function fieldChanged(state, setState) {
  return (event) => {
    setState({ ...state, [event.target.name]: event.target.value });
  };
}

function Preview(props) {
  const bef = props.bef.preview;
  const aft = props.aft.preview;
  const testCount = Math.max(bef.length, aft.length);
  const previewLines = [];
  for (let i = 0; i < testCount; i++) {
    let line = "";
    if (bef[i].is_extra_file) {
      line = bef[i].value;
    } else {
      line = bef[i].value + " => ";
      if (aft[i] != null) {
        line += aft[i].value;
      }
    }
    previewLines.push(line);
  }
  return (
    <Form.Group>
      <Form.Label>Preview</Form.Label>
      <Form.Control as="textarea" value={previewLines.join("\n")} readOnly />
    </Form.Group>
  );
}

function OneSide(props) {
  const { state, setState } = props;
  const onFieldChange = fieldChanged(state, setState);
  return (
    <>
      <Form.Group>
        <Form.Label>Input format</Form.Label>
        <Form.Control
          type="text"
          placeholder="Input format"
          name="inpFormat"
          value={state.inpFormat}
          onChange={onFieldChange}
        />
      </Form.Group>
      <Form.Group>
        <Form.Label>Output format</Form.Label>
        <Form.Control
          type="text"
          placeholder="Output format"
          name="outFormat"
          value={state.outFormat}
          onChange={onFieldChange}
        />
      </Form.Group>
    </>
  );
}

// const history = useHistory();
// const { url } = await api.formatTestSuite({ bef, aft });
// history.push(url);

async function convertTestSuite(fileID, bef, aft, fileName) {
  return await api.convertTestSuite({
    file_id: fileID,
    bef_inp_format: bef.inpFormat,
    bef_out_format: bef.outFormat,
    aft_inp_format: aft.inpFormat,
    aft_out_format: aft.outFormat,
    file_name: fileName,
  });
}

async function previewTestSuite(fileID, bef, aft) {
  return await api.previewTestSuite({
    file_id: fileID,
    bef_inp_format: bef.inpFormat,
    bef_out_format: bef.outFormat,
    aft_inp_format: aft.inpFormat,
    aft_out_format: aft.outFormat,
  });
}

async function getPrefilledInputs(fileID) {
  return await api.getPrefilledInputs({
    file_id: fileID,
  });
}

// function useQuery() {
//   return new URLSearchParams(useLocation().search);
// }

function FileNameInput(props) {
  const { state, setState } = props;
  return (
    <Form.Group>
      <Form.Label>File name</Form.Label>
      <Form.Control type="text" placeholder="File name" value={state} onChange={(e) => setState(e.target.value)} />
    </Form.Group>
  );
}

function ActionButtons(props) {
  const history = useHistory();
  const { fileID, bef, setBef, aft, setAft, fileName } = props;

  return (
    <>
      <Button
        variant="secondary"
        className="mr-1"
        onClick={async () => {
          const { bef_preview, aft_preview } = await previewTestSuite(fileID, bef, aft);
          setBef({ ...bef, preview: bef_preview });
          setAft({ ...aft, preview: aft_preview });
        }}
      >
        Refresh
      </Button>
      <Button
        variant="primary"
        className="mr-2"
        onClick={async () => {
          const { file_id } = await convertTestSuite(fileID, bef, aft, fileName);
          history.push(`/download/${file_id}`);
        }}
      >
        Download
      </Button>
    </>
  );
}

function EditForm(props) {
  const { fileID } = props;
  const [bef, setBef] = useState({ inpFormat: "", outFormat: "", preview: [] });
  const [aft, setAft] = useState({ inpFormat: "", outFormat: "", preview: [] });
  const [fileName, setFileName] = useState("");

  useEffect(() => {
    (async () => {
      const { file_name, inp_format, out_format } = await getPrefilledInputs(fileID);
      setFileName(file_name || "");
      setBef({ inpFormat: inp_format, outFormat: out_format, preview: [] });
    })();
  }, [fileID]);

  return (
    <Form>
      <Row>
        <Col>
          <OneSide state={bef} setState={setBef} />
        </Col>
        <Col>
          <OneSide state={aft} setState={setAft} />
        </Col>
      </Row>
      <Row>
        <Col>
          <Preview bef={bef} aft={aft} />
        </Col>
      </Row>
      <Row>
        <Col>
          <FileNameInput state={fileName} setState={setFileName} />
        </Col>
      </Row>
      <Row>
        <Col>
          <ActionButtons fileID={fileID} bef={bef} setBef={setBef} aft={aft} setAft={setAft} fileName={fileName} />
        </Col>
      </Row>
    </Form>
  );
}

export default function Edit(props) {
  const { fileID } = useParams();

  return (
    <div>
      <TopBar />
      <Container className="container">
        <h1>Format test suite</h1>
        <p>
          Your <a href={api.getDownloadLink(fileID)}>test suite</a> has been uploaded.
        </p>
        <EditForm fileID={fileID} />
      </Container>
    </div>
  );
}
