/**
 * This JavaScript encapsulates the original fetch function,
 * employing functional programming techniques to enhance ease of use.
 * With the help of Chatgpt-3.5 and perplexity.
 */

const getCookieValue = (name) => {
  const cookieString = document.cookie;
  const cookies = cookieString.split(";");
  for (const cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split("=");
    if (cookieName === name) {
      return cookieValue;
    }
  }
  return "";
};

const getJwtToken = () => getCookieValue("access_token");
const getCsrfAccessToken = () => getCookieValue("csrf_access_token");
const getCsrfRefreshToken = () => getCookieValue("csrf_refresh_token");

const jwtHeader = (access_token) => ({
  Authorization: `Bearer ${access_token}`,
});

const csrfHeaders = () => ({
  "X-CSRF-TOKEN-ACCESS": getCsrfAccessToken(),
  "X-CSRF-TOKEN-REFRESH": getCsrfRefreshToken(),
});

const isTokenExpired = (token) => {
  const payloadBase64 = token.split(".")[1];
  const decodedJson = atob(payloadBase64);
  const decoded = JSON.parse(decodedJson);
  const exp = decoded.exp;
  const now = Date.now() / 1000;
  return now > exp;
};

const refreshJwtToken = async () => {
  try {
    const response = await fetch("/auth/refresh", {
      method: "POST",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Token refresh failed");
    }
  } catch (error) {
    console.error("Error refreshing access token:", error);
  }
};

const fetchData = async (url, options = {}) => {
  const access_token = getJwtToken();
  if (access_token && isTokenExpired(access_token)) {
    await refreshJwtToken();
  }
  options.headers = {
    ...options.headers,
    ...jwtHeader(access_token),
    ...(options.method !== "GET" ? csrfHeaders() : {}),
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
