import JSZip from "jszip";

type FileCheckResult = {
    isValid: boolean;
    missingFiles: string[];
};

/**
 * Checks if the zipObject contains at least all the files that match the regexList
 * 
 * @param zipObject - JSZip object to match the regex against
 * @param regexList - List of regex strings to match against the zipObject
 * 
 * @returns true if all regex strings are found in the zipObject, false otherwise
 */
export function verifyZipContents(zipObject: JSZip, regexList: string[]): FileCheckResult{
    const missingFiles: string[] = [];
    const status = regexList.every((regex) => {
        let found: boolean = false;
        zipObject.forEach((relativePath, _) => {
            if (new RegExp(regex).test(relativePath)) {
                found = true;
            }
        });
        if (!found) {
            missingFiles.push(regex);
        }
        return found;
    });

    return {"isValid": status, "missingFiles": missingFiles };
}
