import React from "react";
import { useParams } from "react-router-dom";
import * as api from "../../api";

export default function Download() {
  const { fileID } = useParams();
  api.downloadFile(fileID);
  return <pre>Downloading...</pre>;
}
