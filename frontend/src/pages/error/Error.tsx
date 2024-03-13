import { isRouteErrorResponse, useRouteError } from "react-router-dom"

export function Error() {
    const error = useRouteError();

    if (isRouteErrorResponse(error)) {

        let message = "";
        if (error.status == 403) {
            message = "Forbidden"
        } else if (error.status == 404) {
            message = "Page not found";
        } else if (error.status == 500) {
            message = "Internal server error";
        } else if (error.status == 503) {
            message = "Looks like our API is down";
        } else if (500 <= error.status && error.status <= 599) {
            message = "General server error";
        }

        return(
            <div>
                <p>
                    { error.status }
                </p>
                <p>
                    { message }
                </p>
            </div>
        )
    }
}