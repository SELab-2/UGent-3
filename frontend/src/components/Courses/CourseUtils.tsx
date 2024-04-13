import { NavigateFunction } from 'react-router-dom';

export interface Course{
    course_id: string,
    name: string,
    teacher:string,
    ufora_id:string,
    url:string
}

export interface Project{
    title: string,
    project_id: string,
    deadlines: Deadline[]
}

interface Deadline{
  description:string,
  deadline:string
}

export const apiHost = import.meta.env.VITE_API_HOST;
/**
 * @returns The uid of the acces token of the logged in user
 */
export function loggedInToken(){
  return "teacher1";
}
    
/**
 * @returns The Uid of the logged in user
 */
export function loggedInUid(){
  return "Gunnar";
}

/**
 * On a succesfull fetch the function will redirect to the data.url of the response
 * @param path - path to backend api endpoint
 * @param data - optional data to send to the api
 * @param method - POST, GET, PATCH, DELETE
 * @param navigate - function that allows the app to redirect
 */
export function callToApi(path: string, data: string, method:string, navigate: NavigateFunction){
  
  fetch(path, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': loggedInToken()
    },
    body: data,
  })
    .then(response => response.json())
    .then(data => {
      navigate(getIdFromLink(data.url)); // navigate to data.url
    })
    .catch((error) => {
      console.error('Error:', error); //should redirect to error page
    });
}
  
/**
 * @param link - the link to the api endpoint
 * @returns the Id at the end of the link
 */
export function getIdFromLink(link: string): string {
  const parts = link.split('/');
  return parts[parts.length - 1];
}

/**
 * Function to find the nearest future date from a list of dates
 * @param dates - Array of dates
 * @returns The nearest future date
 */
export function getNearestFutureDate(dates: Deadline[]): Date | null {
  const now = new Date();
  const futureDates = dates.map(date => new Date(date.deadline)).filter(date => date > now);
  if (futureDates.length === 0) return null;
  return futureDates.reduce((nearest, current) => current < nearest ? current : nearest);
}