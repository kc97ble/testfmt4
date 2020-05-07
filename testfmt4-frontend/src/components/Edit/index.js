import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useHistory, useParams } from "react-router-dom";
import * as api from "../../api";

function fieldChanged(state, setState) {
  return (event) => {
    setState({ ...state, [event.target.name]: event.target.value });
  };
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
      <Form.Group>
        <Form.Label>Preview</Form.Label>
        <Form.Control as="textarea" value={state.preview.join("\n")} readOnly />
      </Form.Group>
    </>
  );
}

async function convertTestSuite(fileID, bef, aft) {
  // const history = useHistory();
  // const { url } = await api.formatTestSuite({ bef, aft });
  // history.push(url);
  return await api.convertTestSuite({
    uploaded_file_id: fileID,
    bef_inp_format: bef.inpFormat,
    bef_out_format: bef.outFormat,
    aft_inp_format: aft.inpFormat,
    aft_out_format: aft.outFormat,
  });
}

async function previewTestSuite(fileID, bef, aft) {
  return await api.previewTestSuite({
    uploaded_file_id: fileID,
    bef_inp_format: bef.inpFormat,
    bef_out_format: bef.outFormat,
    aft_inp_format: aft.inpFormat,
    aft_out_format: aft.outFormat,
  });
}

// function useQuery() {
//   return new URLSearchParams(useLocation().search);
// }

function EditForm(props) {
  const { fileID } = props;
  const history = useHistory();
  const [bef, setBef] = useState({ inpFormat: "", outFormat: "", preview: [] });
  const [aft, setAft] = useState({ inpFormat: "", outFormat: "", preview: [] });
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
      <Button
        variant="secondary"
        onClick={async () => {
          const { bef_preview, aft_preview } = await previewTestSuite(
            fileID,
            bef,
            aft
          );
          setBef({ ...bef, preview: bef_preview });
          setAft({ ...aft, preview: aft_preview });
        }}
      >
        Refresh
      </Button>
      <Button
        variant="primary"
        onClick={async () => {
          const { file_id } = await convertTestSuite(fileID, bef, aft);

          history.push(`/download/${file_id}`);
        }}
      >
        Download
      </Button>
    </Form>
  );
}

export default function Edit(props) {
  const { fileID } = useParams();

  return (
    <Container>
      <Row>
        <Col>
          <pre>{fileID}</pre>
          <EditForm fileID={fileID} />
        </Col>
      </Row>
    </Container>
  );
}
