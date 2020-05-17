import React, { useState, useEffect, useRef } from "react";
import { Container, Row, Col } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Spinner from "react-bootstrap/Spinner";
import { useHistory, useParams } from "react-router-dom";
import * as api from "../../api";
import TopBar from "../../common/TopBar";
import "../../common/sharedStyles.css";
import "./styles.css";

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
      <Form.Control rows="10" as="textarea" value={previewLines.join("\n")} readOnly />
    </Form.Group>
  );
}

function OneSide(props) {
  const { state, setState, label } = props;
  const onFieldChange = fieldChanged(state, setState);
  return (
    <>
      <Form.Group>
        <Form.Label>
          <strong>{label}</strong>
        </Form.Label>
      </Form.Group>
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

async function convertTestSuite(fileID, bef, aft, fileName) {
  const data = await api.convertTestSuite({
    file_id: fileID,
    bef_inp_format: bef.inpFormat,
    bef_out_format: bef.outFormat,
    aft_inp_format: aft.inpFormat,
    aft_out_format: aft.outFormat,
    file_name: fileName,
  });
  console.log(data);

  return {
    fileID: data.file_id,
    errorMsg: data.error_msg,
  };
}

async function previewTestSuite(fileID, befInpFormat, befOutFormat, aftInpFormat, aftOutFormat) {
  const data = await api.previewTestSuite({
    file_id: fileID,
    bef_inp_format: befInpFormat,
    bef_out_format: befOutFormat,
    aft_inp_format: aftInpFormat,
    aft_out_format: aftOutFormat,
  });
  return {
    befPreview: data.bef_preview,
    aftPreview: data.aft_preview,
    errorMsg: data.error_msg,
  };
}

async function getPrefilledInputs(fileID) {
  const data = await api.getPrefilledInputs({ file_id: fileID });
  return {
    inpFormat: data.inp_format,
    outFormat: data.out_format,
    fileName: data.file_name,
    errorMsg: data.error_msg,
  };
}

function FileNameInput(props) {
  const { state, setState } = props;
  return (
    <Form.Group>
      <Form.Label>File name</Form.Label>
      <Form.Control type="text" placeholder="File name" value={state} onChange={(e) => setState(e.target.value)} />
    </Form.Group>
  );
}

function RefreshButton(props) {
  const { loading, onClick, buttonRef } = props;

  const caption = loading ? "Refreshing..." : "Refresh";
  return (
    <Button variant="secondary" className="mr-1 long-button" onClick={onClick} disabled={loading} ref={buttonRef}>
      {caption}
    </Button>
  );
}

function DownloadButton(props) {
  const { onClick } = props;
  const [loading, setLoading] = useState(false);
  const caption = loading ? "Downloading..." : "Download";
  return (
    <Button
      variant="primary"
      className="mr-1 long-button"
      onClick={async (e) => {
        setLoading(true);
        await onClick(e);
        setLoading(false);
      }}
      disabled={loading}
    >
      {caption}
    </Button>
  );
}

const DEFAULT_BEF = { inpFormat: "", outFormat: "", preview: [] };
const DEFAULT_AFT = { inpFormat: "input.000", outFormat: "output.000", preview: [] };

function EditForm(props) {
  const { fileID } = props;
  const history = useHistory();

  const [bef, setBef] = useState(DEFAULT_BEF);
  const [aft, setAft] = useState(DEFAULT_AFT);
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(true);

  const [refreshing, setRefreshing] = useState(false);
  const refreshButton = useRef(null);

  const onRefresh = async () => {
    if (refreshing) return;
    setRefreshing(true);
    const { befPreview, aftPreview, errorMsg } = await previewTestSuite(
      fileID,
      bef.inpFormat,
      bef.outFormat,
      aft.inpFormat,
      aft.outFormat
    );
    if (errorMsg) {
      alert(errorMsg);
    } else {
      setBef((bef) => ({ ...bef, preview: befPreview }));
      setAft((aft) => ({ ...aft, preview: aftPreview }));
    }
    setRefreshing(false);
  };

  const onDownload = async () => {
    const data = await convertTestSuite(fileID, bef, aft, fileName);
    if (data.errorMsg) {
      alert(data.errorMsg);
    } else {
      history.push(`/download/${data.fileID}`);
    }
  };

  useEffect(() => {
    (async () => {
      const { fileName, inpFormat, outFormat, errorMsg } = await getPrefilledInputs(fileID);
      if (errorMsg) {
        alert(errorMsg);
      } else {
        setFileName(fileName || "");
        setBef((bef) => ({ ...bef, inpFormat: inpFormat, outFormat: outFormat }));
      }

      const previewData = await previewTestSuite(
        fileID,
        inpFormat,
        outFormat,
        DEFAULT_AFT.inpFormat,
        DEFAULT_AFT.outFormat
      );
      if (previewData.errorMsg) {
        alert(previewData.errorMsg);
      } else {
        setBef((bef) => ({ ...bef, preview: previewData.befPreview }));
        setAft((aft) => ({ ...aft, preview: previewData.aftPreview }));
      }
      setLoading(false);
    })();
  }, [fileID]);

  useEffect(() => {
    const handler = setTimeout(() => refreshButton.current.click(), 500);
    return () => clearTimeout(handler);
  }, [bef.inpFormat, bef.outFormat, aft.inpFormat, aft.outFormat]);

  return (
    <div className="mt-4">
      <Row style={{ display: loading ? "block" : "none" }}>
        <Col style={{ display: "flex", justifyContent: "center" }}>
          <Spinner animation="border" />
        </Col>
      </Row>
      <Row style={{ display: loading ? "none" : "block" }}>
        <Col>
          <Form>
            <Row>
              <Col>
                <OneSide label="Before" state={bef} setState={setBef} />
              </Col>
              <Col>
                <OneSide label="After" state={aft} setState={setAft} />
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
                <RefreshButton buttonRef={refreshButton} loading={refreshing} onClick={onRefresh} />
                <DownloadButton onClick={onDownload} />
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
    </div>
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
