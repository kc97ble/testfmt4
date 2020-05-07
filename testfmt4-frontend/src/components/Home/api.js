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
}
