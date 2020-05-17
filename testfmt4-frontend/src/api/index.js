import dotenv from "dotenv";
dotenv.config();

const BACKEND = process.env.REACT_APP_BACKEND || "http://localhost:5000";

function getFormDataFromParams(params, keys) {
  const formData = new FormData();
  keys.forEach((k) => {
    if (k in params) {
      formData.append(k, params[k]);
    } else {
      throw new Error("Missing parameter");
    }
  });
  return formData;
}

function filterKeys(obj, keys) {
  const result = {};
  keys.forEach((k) => {
    result[k] = obj[k];
  });
  return result;
}

export async function uploadFile(params) {
  const requiredKeys = ["file"];
  const formData = getFormDataFromParams(params, requiredKeys);
  const response = await fetch(`${BACKEND}/upload`, { method: "POST", body: formData });
  return await response.json();
}

export async function previewTestSuite(params) {
  const requiredKeys = ["file_id", "bef_inp_format", "bef_out_format", "aft_inp_format", "aft_out_format"];
  const formData = getFormDataFromParams(params, requiredKeys);
  const response = await fetch(`${BACKEND}/preview`, { method: "POST", body: formData });
  const data = await response.json();
  const expectedKeys = ["bef_preview", "aft_preview"];
  return filterKeys(data, expectedKeys);
}

export async function convertTestSuite(params) {
  const requiredKeys = ["file_id", "bef_inp_format", "bef_out_format", "aft_inp_format", "aft_out_format", "file_name"];
  const formData = getFormDataFromParams(params, requiredKeys);
  const response = await fetch(`${BACKEND}/convert`, { method: "POST", body: formData });
  const data = await response.json();
  const expectedKeys = ["file_id"];
  return filterKeys(data, expectedKeys);
}

export async function getPrefilledInputs(params) {
  const requiredKeys = ["file_id"];
  const formData = getFormDataFromParams(params, requiredKeys);
  const response = await fetch(`${BACKEND}/prefill`, { method: "POST", body: formData });
  const data = await response.json();
  const expectedKeys = ["inp_format", "out_format", "file_name"];
  return filterKeys(data, expectedKeys);
}

export function getDownloadLink(fileID) {
  return `${BACKEND}/download/${fileID}`;
}

export function downloadFile(fileID) {
  window.location.href = getDownloadLink(fileID);
}

export async function previewFile(fileID) {
  const response = await fetch(`${BACKEND}/preview_file/${fileID}`);
  const data = await response.json();
  const expectedKeys = ["file_name", "file_size", "content"];
  return filterKeys(data, expectedKeys);
}
