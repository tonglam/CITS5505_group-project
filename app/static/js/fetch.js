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
  return cookies;
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

const getJwtToken = () => {
  if (!cookies.access_token) {
    // Attempt to get it from document.cookie if it exists there
    const match = document.cookie.match(/(^|;)\s*access_token\s*=\s*([^;]+)/);
    return match ? match[2] : "";
  }
  return cookies.access_token;
};

const getCsrfAccessToken = () => {
  if (!cookies.csrf_access_token) {
    // Attempt to get it from document.cookie if it exists there
    const match = document.cookie.match(
      /(^|;)\s*csrf_access_token\s*=\s*([^;]+)/
    );
    return match ? match[2] : "";
  }
  return cookies.csrf_access_token;
};

const getCsrfRefreshToken = () => {
  if (!cookies.csrf_refresh_token) {
    // Attempt to get it from document.cookie if it exists there
    const match = document.cookie.match(
      /(^|;)\s*csrf_refresh_token\s*=\s*([^;]+)/
    );
    return match ? match[2] : "";
  }
  return cookies.csrf_refresh_token;
};

const getRefreshToken = () => {
  if (!cookies.refresh_token) {
    // Attempt to get it from document.cookie if it exists there
    const match = document.cookie.match(/(^|;)\s*refresh_token\s*=\s*([^;]+)/);
    return match ? match[2] : "";
  }
  return cookies.refresh_token;
};

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
  if (!token) return true;

  try {
    const payloadBase64 = token
      .split(".")[1]
      .replace(/-/g, "+")
      .replace(/_/g, "/");
    const decodedJson = atob(payloadBase64);
    const decoded = JSON.parse(decodedJson);
    const now = Date.now() / 1000;
    return decoded.exp < now;
  } catch (error) {
    console.error("Error checking token expiration:", error);
    return true;
  }
};

async function refreshToken() {
  try {
    await getCookieValue();
    const csrfRefreshToken = getCsrfRefreshToken();

    const response = await fetch("/auth/refresh", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRF-Token": csrfRefreshToken,
      },
    });

    if (!response.ok) {
      throw new Error("Token refresh failed");
    }

    await new Promise((resolve) => setTimeout(resolve, 100));

    await getCookieValue();
    return true;
  } catch (error) {
    console.error("Error refreshing token:", error);
    return false;
  }
}

async function fetchData(url, options = {}) {
  try {
    // Always get fresh tokens before making a request
    await getCookieValue();
    let accessToken = getJwtToken();
    let csrfToken = getCsrfAccessToken();

    // Add headers
    options.headers = {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
      "X-CSRF-TOKEN": csrfToken,
    };

    // Make the request
    const response = await fetch(url, {
      ...options,
      credentials: "same-origin",
    });

    // Handle different response statuses
    if (response.status === 401) {
      const refreshSuccess = await refreshToken();
      if (refreshSuccess) {
        // Wait for cookies to be updated
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Get fresh tokens after refresh
        await getCookieValue();
        accessToken = getJwtToken();
        csrfToken = getCsrfAccessToken();

        // Retry original request with new token
        const retryResponse = await fetch(url, {
          ...options,
          credentials: "same-origin",
          headers: {
            ...options.headers,
            Authorization: `Bearer ${accessToken}`,
            "X-CSRF-TOKEN": csrfToken,
          },
        });

        if (!retryResponse.ok) {
          throw new Error(`HTTP error! status: ${retryResponse.status}`);
        }

        return await processResponse(retryResponse);
      } else {
        // Refresh failed, redirect to login
        window.location.href = "/auth/auth";
        return null;
      }
    }

    // Handle other error statuses
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await processResponse(response);
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

async function processResponse(response) {
  // Return the response as is for 204 No Content
  if (response.status === 204) {
    return response;
  }

  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    return await response.json();
  }
  return await response.text();
}

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
    return await fetchData(getUrl, { headers: getHeaders });
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
