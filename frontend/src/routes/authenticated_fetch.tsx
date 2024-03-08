/**
 *
 * @param {string} url - The URL to fetch.
 * @returns The fetch response.
 */
export function authenticated_fetch(url:string){
  return fetch(url+"?uid=user1")
}