import {Deadline} from "../../../types/deadline.ts";

/**
 *
 */
export default function ProjectAdminViewDeadlineDatagrid({ deadlines }) {
  return (
    <div>
      {deadlines.map((deadline: Deadline, index) => (
        <p key={index}>{deadline}</p>
      ))}
    </div>
  );
}
