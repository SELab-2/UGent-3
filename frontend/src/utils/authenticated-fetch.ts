import { getCSRFCookie } from "./csrf";

/**
 * A helper function to automatically add the necessary authentication options to fetch
 * @returns the result of the fetch with given options and default authentication options included
 */
export function authenticatedFetch(
  url: string | URL | globalThis.Request,
  init?: RequestInit
): Promise<Response> {
  const update = { ...init,  credentials: "include"};
  update.headers = {
    ...update.headers,
    "X-CSRF-TOKEN": getCSRFCookie()
  }
  return fetch(url, Object.assign(update));
}
