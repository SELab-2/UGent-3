import { useEffect, useState } from "react";
import { fetchMe } from "../../utils/fetches/FetchMe";
import { CourseDetailStudent } from "./CourseDetailStudent";
import { CourseDetailTeacher } from "./CourseDetailTeacher";
import { Me } from "../../types/me";

/**
 *
 * @returns The right course detail component according to the role of the user.
 */
export function CourseDetail(): JSX.Element {
  const [me, setMe] = useState<Me | null>(null);

  useEffect(() => {
    fetchMe().then((data) => {
      setMe(data);
    });
  }, []);

  if (me?.role === "STUDENT") {
    return <CourseDetailStudent />;
  }
  if (me === undefined) {
    return <></>;
  }
  return <CourseDetailTeacher />;
}