/**
 * This JavaScript encapsulates the original fetch function,
 * employing functional programming techniques to enhance ease of use.
 * With the help of Chatgpt-3.5 and perplexity.
 */

let cookies = {};

$(document).ready(function () {
  getCookieValue();
});

const getCookieValue = async () => {
  const response = await getCookies();
  if (response.toLowerCase().includes("<!doctype html>")) {
    return false;
  }
  cookies = JSON.parse(response);
};

const getCookies = async () => {
  try {
    const response = await fetch("/auth/cookies");
    if (!response.ok) {
      console.error(`HTTP error! Status: ${response.status}`);
    }
    return await response.text();
  } catch (error) {
    console.error("Error:", error);
  }
};

const getJwtToken = () => cookies.access_token;
const getCsrfAccessToken = () => cookies.csrf_access_token;
const getCsrfRefreshToken = () => cookies.csrf_refresh_token;

const jwtHeader = (access_token) => ({
  "X-CSRF-TOKEN": getCsrfAccessToken(),
  Authorization: `Bearer ${access_token}`,
});

const csrfHeaders = () => ({
  "X-CSRF-TOKEN": getCsrfAccessToken(),
  "X-CSRF-TOKEN-ACCESS": getCsrfAccessToken(),
  "X-CSRF-TOKEN-REFRESH": getCsrfRefreshToken(),
});

const isTokenExpired = (token) => {
  const payloadBase64 = token
    .split(".")[1]
    .replace(/-/g, "+")
    .replace(/_/g, "/");
  const decodedJson = atob(payloadBase64);
  const decoded = JSON.parse(decodedJson);
  const now = Date.now() / 1000;
  return decoded.exp < now;
};

const fetchData = async (url, options = {}) => {
  const access_token = getJwtToken();
  if (isTokenExpired(access_token)) {
    window.location.href = "/auth/logout";
    return false;
  }

  options.headers = {
    ...options.headers,
    ...jwtHeader(access_token),
  };

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
    const urlObject = new URL(url, window.location.origin);
    const params = urlObject.searchParams;
    Object.entries(data).forEach(([key, value]) => {
      params.set(key, value);
    });
    const getUrl = `${urlObject.pathname}${urlObject.search}`;
    const access_token = getJwtToken();
    const getHeaders = { ...jwtHeader(access_token), ...headers };
    return await fetchData(getUrl, { getHeaders });
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

const putFetch =
  (url) =>
  (data = {}) =>
  async (headers = {}) => {
    const access_token = getJwtToken();
    const putHeaders = { ...jwtHeader(access_token), ...headers };
    const options = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...putHeaders,
      },
      body: JSON.stringify(data),
    };
    return await fetchData(url, options);
  };

const deleteFetch =
  (url) =>
  (data = {}) =>
  async (headers = {}) => {
    const access_token = getJwtToken();
    const deleteHeaders = { ...jwtHeader(access_token), ...headers };
    const options = {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        ...deleteHeaders,
      },
      body: JSON.stringify(data),
    };
    return await fetchData(url, options);
  };
