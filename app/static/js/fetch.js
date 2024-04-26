/**
 * This JavaScript encapsulates the original fetch function,
 * employing functional programming techniques to enhance ease of use.
 * With the help of Chatgpt-3.5.
 */

const getJwtToken = () => {
  const cookieString = document.cookie;
  const cookies = cookieString.split(";");
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split("=");
    if (name === "access_token") {
      return value;
    }
  }
  return "";
};
const jwtHeader = (access_token) => ({
  Cookie: `access_token=${access_token}`,
});

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
    const access_token = getJwtToken();
    const getHeaders = { ...jwtHeader(access_token), ...headers };
    return await fetchData(apiUrl, { getHeaders });
  };

const postFetch =
  (url) =>
  (data = {}) =>
  async (headers = {}) => {
    const access_token = getJwtToken();
    const postHeaders = { ...jwtHeader(access_token), ...headers };

    let options = {};
    if (data instanceof FormData) {
      options = {
        method: "POST",
        body: data,
        headers: postHeaders,
      };
    } else {
      options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...postHeaders,
        },
        body: JSON.stringify(data),
      };
    }

    return await fetchData(url, options);
  };

export { getFetch, getFetchWithToken, postFetch, postFetchWithToken };
