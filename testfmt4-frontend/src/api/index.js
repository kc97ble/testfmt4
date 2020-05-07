const BACKEND = "http://localhost:5000";

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("foo", "bar");
  formData.append("file", file);
  const response = await fetch(`${BACKEND}/upload`, {
    method: "POST",
    body: formData,
  });
  const { uploaded_file_id } = await response.json();
  console.log({ uploaded_file_id });
  return { uploaded_file_id };
}

export async function previewTestSuite(params) {
  const {
    uploaded_file_id,
    bef_inp_format,
    bef_out_format,
    aft_inp_format,
    aft_out_format,
  } = params;
  const formData = new FormData();
  formData.append("uploaded_file_id", uploaded_file_id);
  formData.append("bef_inp_format", bef_inp_format);
  formData.append("bef_out_format", bef_out_format);
  formData.append("aft_inp_format", aft_inp_format);
  formData.append("aft_out_format", aft_out_format);
  const response = await fetch(`${BACKEND}/preview`, {
    method: "POST",
    body: formData,
  });
  const { bef_preview, aft_preview } = await response.json();
  return { bef_preview, aft_preview };
}

export async function convertTestSuite(params) {
  const {
    uploaded_file_id,
    bef_inp_format,
    bef_out_format,
    aft_inp_format,
    aft_out_format,
  } = params;
  const formData = new FormData();
  formData.append("uploaded_file_id", uploaded_file_id);
  formData.append("bef_inp_format", bef_inp_format);
  formData.append("bef_out_format", bef_out_format);
  formData.append("aft_inp_format", aft_inp_format);
  formData.append("aft_out_format", aft_out_format);
  const response = await fetch(`${BACKEND}/convert`, {
    method: "POST",
    body: formData,
  });
  const { file_id } = await response.json();
  return { file_id };
}

export function downloadFile(fileID) {
  window.location.href = `${BACKEND}/download/${fileID}`;
}
