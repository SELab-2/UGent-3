export function authenticated_fetch(url:string){
    return fetch(url+"?uid=user1")
}