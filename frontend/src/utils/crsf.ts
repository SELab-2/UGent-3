export function get_csrf_cookie(): string {
    const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrf_access_token="))
    ?.split("=")[1];
    if(!cookie) {
        return "";
    }
    return cookie;
}