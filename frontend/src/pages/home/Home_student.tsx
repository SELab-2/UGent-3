import { useTranslation } from "react-i18next";
import {Card, CardContent, Typography, Grid, Container, Badge} from '@mui/material';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import {DayCalendarSkeleton, LocalizationProvider} from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import React, {useEffect, useState} from 'react';
import dayjs, {Dayjs} from "dayjs";
import { PickersDay, PickersDayProps } from '@mui/x-date-pickers/PickersDay';
import {ProjectDeadlineCard} from "../project/projectDeadline/ProjectDeadlineCard.tsx";
import {ProjectDeadline, ShortSubmission} from "../project/projectDeadline/ProjectDeadline.tsx";

const apiUrl = import.meta.env.VITE_APP_API_URL
const initialValue = dayjs(Date.now());

interface DeadlineInfoProps {
  selectedDay: Dayjs;
  deadlines: ProjectDeadline[];
}

type ExtendedPickersDayProps = PickersDayProps<Dayjs> & { highlightedDays?: number[] };

/**
 * Displays the deadlines on a given day
 * @param selectedDay - The day of interest
 * @param deadlines - All the deadlines to consider
 * @returns Element
 */
const DeadlineInfo: React.FC<DeadlineInfoProps> = ({ selectedDay, deadlines }) => {
  const { t } = useTranslation('translation', { keyPrefix: 'student' });
  const deadlinesOnSelectedDay = deadlines.filter(
    deadline => ( deadline.deadlines.map(d => dayjs(d.deadline).isSame(selectedDay, 'day')))
  );
  //list of the corresponding assignment
  return (
    <div>
      {deadlinesOnSelectedDay.length === 0 ? (
        <Card style={{margin: '10px 0'}}>
          <CardContent>
            <Typography variant="body1">
              {t('noDeadline')}
            </Typography>
          </CardContent>
        </Card>
      ) : <ProjectDeadlineCard deadlines={deadlinesOnSelectedDay}/>}
    </div>
  );
};

/**
 *
 * @param props - The day and the deadlines
 * @returns - The ServerDay component that displays a badge for specific days
 */
function ServerDay(props: PickersDayProps<Dayjs> & { highlightedDays?: number[] }) {
  const { highlightedDays = [], day, outsideCurrentMonth, ...other } = props;

  const isSelected =
    !props.outsideCurrentMonth && highlightedDays.indexOf(props.day.date()) >= 0;

  return (
    <Badge
      key={props.day.toString()}
      overlap="circular"
      badgeContent={isSelected ? '🔴' : undefined}
      sx={{
        '.MuiBadge-badge': {
          fontSize: '0.5em',
          top: 8,
          right: 8,
        },
      }}
    >
      <PickersDay {...other} outsideCurrentMonth={outsideCurrentMonth} day={day} />
    </Badge>
  );
}
const handleMonthChange =(
  date: Dayjs,
  projects:ProjectDeadline[],
  setHighlightedDays: React.Dispatch<React.SetStateAction<number[]>>,
) => {

  setHighlightedDays([]);
  // projects are now only fetched on page load
  const hDays:number[] = []
  projects.map((project, ) => {
    project.deadlines.map((deadline,) => {
      if(deadline.deadline.getMonth() == date.month() && deadline.deadline.getFullYear() == date.year()){
        hDays.push(deadline.deadline.getDate())
      }
    })

  }
  );
  setHighlightedDays(hDays)

};
const fetchProjects = async (setProjects: React.Dispatch<React.SetStateAction<ProjectDeadline[]>>) => {
  const header  = {
    "Authorization": "teacher2" // todo add true authorization
  }
  const response = await fetch(`${apiUrl}/projects`, {
    headers:header
  })
  const jsonData = await response.json();
  const formattedData: ProjectDeadline[] = await Promise.all( jsonData.data.map(async (item:ProjectDeadline) => {
    console.log("project", item)
    const project_id:string = item.project_id.split("/")[1]// todo check if this does not change later

    const response_submissions = await (await fetch(encodeURI(`${apiUrl}/submissions?&project_id=${project_id}`), {
      headers: header
    })).json()

    //get the latest submission
    const latest_submission = response_submissions.data.map((submission:ShortSubmission) => ({
      submission_id: submission.submission_id,//this is the path 
      submission_time: new Date(submission.submission_time),
      submission_status: submission.submission_status
    }
    )).sort((a:ShortSubmission, b:ShortSubmission) => b.submission_time.getTime() - a.submission_time.getTime())[0];
    // fetch the course id of the project
    const project_item = await (await fetch(encodeURI(`${apiUrl}/${item.project_id}`), { //todo !
      headers:header
    })).json()

    //fetch the course
    const response_courses = await (await fetch(encodeURI(`${apiUrl}/courses/${project_item.data.course_id}`), {
      headers: header
    })).json()
    const course = {
      course_id: response_courses.data.course_id,
      name: response_courses.data.name,
      teacher: response_courses.data.teacher,
      ufora_id: response_courses.data.ufora_id
    }
    return  {
      project_id: item.project_id, //todo is not a number but a path
      title: item.title,
      description: item.description,
      assignment_file: item.assignment_file,
      deadlines: [{description: "", deadline: new Date()}],
      course_id: Number(item.course_id),
      visible_for_students: Boolean(item.visible_for_students),
      archived: Boolean(item.archived),
      test_path: item.test_path,
      script_name: item.script_name,
      regex_expressions: item.regex_expressions,
      short_submission: latest_submission,
      course: course
    }}));
  setProjects(formattedData);
  return formattedData
}

/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function HomeStudent() {
  const { t } = useTranslation('translation', { keyPrefix: 'student' });

  const [projects, setProjects] = useState<ProjectDeadline[]>([]);

  const [highlightedDays, setHighlightedDays] = React.useState<number[]>([]);

  const [selectedDay, setSelectedDay] = useState<Dayjs>(dayjs(Date.now()));

  useEffect(() => {
    fetchProjects(setProjects).then(p => {
      handleMonthChange(initialValue, p,setHighlightedDays)
    })
  }, []);

  // Update selectedDay state when a day is selected
  const handleDaySelect = (day: Dayjs) => {
    setSelectedDay(day);
  };

  return (
    <Container style={{ paddingTop: '50px' }}>
      <Grid container spacing={2} wrap="nowrap">
        <Grid item xs={6}>
          <Typography variant="body2">
            {t('myProjects')}
          </Typography>

          <ProjectDeadlineCard pred = {(d) => (dayjs(dayjs()).isBefore(d.deadline))} deadlines={projects} />

        </Grid>
        <Grid item xs={6}>
          <Typography variant="body2">
            {t('deadlines')}
          </Typography>
          <ProjectDeadlineCard pred={(d) => dayjs(dayjs()).isAfter(d.deadline)} deadlines={projects} />
        </Grid>
        <Grid item xs={6}>
          <Card>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DateCalendar
                value={selectedDay}
                onMonthChange={(date:Dayjs) => {handleMonthChange(date, projects,
                  setHighlightedDays)}}
                onChange={handleDaySelect}
                renderLoading={() => <DayCalendarSkeleton />}
                slots={{
                  day: ServerDay,
                }}
                slotProps={{
                  day: {
                    highlightedDays,
                  } as ExtendedPickersDayProps,
                }}
              />
            </LocalizationProvider>
            <CardContent>
              <Typography variant="body2">
                {t('deadlinesOnDay')} {selectedDay.format('MMMM D, YYYY')}
              </Typography>
              <DeadlineInfo selectedDay={selectedDay} deadlines={projects} />
            </CardContent>

          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}
