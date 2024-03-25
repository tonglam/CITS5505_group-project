/**
 * This JavaScript encapsulates the original fetch function,
 * employing functional programming techniques to enhance ease of use.
 * With the help of Chatgpt-3.5.
 */

const fetchData = async (url, options = {}) => {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      console.error(`HTTP error! Status: ${response.status}`);
    }
    const contentType = response.headers.get("Content-Type");
    if (contentType && contentType.includes("application/json")) {
      return await response.json();
    } else {
      return await response.text();
    }
  } catch (error) {
    console.error("Error:", error);
  }
};

const getFetch =
  (url) =>
  (data = {}) =>
  async (headers = {}) => {
    const queryParams = new URLSearchParams(data).toString();
    const apiUrl = queryParams ? `${url}?${queryParams}` : url;
    return await fetchData(apiUrl, { headers });
  };

const postFetch =
  (url) =>
  (data = {}) =>
  async (headers = {}) => {
    let options = {};

    if (data instanceof FormData) {
      options = {
        method: "POST",
        body: data,
        headers: headers,
      };
    } else {
      options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...headers,
        },
        body: JSON.stringify(data),
      };
    }

    return await fetchData(url, options);
  };

export { getFetch, postFetch };
