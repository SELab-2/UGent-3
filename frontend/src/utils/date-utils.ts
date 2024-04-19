import i18next from "i18next";

/**
 *
 * @param date - date string to be converted to time difference
 * @returns - time difference between the current date and the given date
 */
export function timeDifference(date: string, past: boolean = false) {
  const t = (key: string) => {
    return i18next.t(`time.${key}`);
  };

  const current = new Date();
  const previous = new Date(date);
  let diff = 0;
  if (past) {
    diff = current.getTime() - previous.getTime();
  } else {
    diff = previous.getTime() - current.getTime();
  }
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const months = Math.floor(days / 30);
  const years = Math.floor(months / 12);
  if (past) {
    if (years > 0) return `${years} ${t("yearsAgo")}`;
    if (months > 0) return `${months} ${t("monthsAgo")}`;
    if (days > 0) return `${days} ${t("daysAgo")}`;
    if (hours > 0) return `${hours} ${t("hoursAgo")}`;
    if (minutes > 0) return `${minutes} ${t("minutesAgo")}`;
  }
  else{
    if (years > 0) return `${years} ${t("yearsLater")}`;
    if (months > 0) return `${months} ${t("monthsLater")}`;
    if (days > 0) return `${days} ${t("daysLater")}`;
    if (hours > 0) return `${hours} ${t("hoursLater")}`;
    if (minutes > 0) return `${minutes} ${t("minutesLater")}`;
  }
  return t("justNow");
}
