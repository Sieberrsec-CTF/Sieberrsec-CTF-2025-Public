function getQueryParams() {
  const params = new URLSearchParams(window.location.search);
  const result = {};
  for (const [key, value] of params.entries()) {
    result[key] = value;
  }
  return result;
}

params = getQueryParams();

// what am i even doing
fetch(`/serve/${params.filename}${window.location.search}`).then(response => {
    return response.text();
  }).then(data => {
    document.querySelector("#content").innerHTML = `Here is your rendered content!
${data}
${document.cookie}
Enjoy! :'>`;
  });