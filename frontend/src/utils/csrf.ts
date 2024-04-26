/**
 * A helper function to easily retrieve the crsf_access_token cookie
 * @returns the crsf_access_token cookie
 */
export function getCSRFCookie(): string {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrf_access_token="))
    ?.split("=")[1];
  return cookie ? cookie : "";
}
