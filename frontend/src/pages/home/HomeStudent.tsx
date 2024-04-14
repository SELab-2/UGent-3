import { useTranslation } from "react-i18next";
import {Card, CardContent, Typography, Grid, Container, Badge} from '@mui/material';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import {DayCalendarSkeleton, LocalizationProvider} from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import React, {useEffect, useState} from 'react';
import dayjs, {Dayjs} from "dayjs";
import { PickersDay, PickersDayProps } from '@mui/x-date-pickers/PickersDay';
import {ProjectDeadlineCard} from "../project/projectDeadline/ProjectDeadlineCard.tsx";
import {ProjectDeadline, ShortSubmission, Project} from "../project/projectDeadline/ProjectDeadline.tsx";

const API_URL = import.meta.env.VITE_APP_API_URL
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
    project => (project.deadline && dayjs(project.deadline).isSame(selectedDay, 'day'))
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
    if(project.deadline && project.deadline.getMonth() == date.month() && project.deadline.getFullYear() == date.year()){
      hDays.push(project.deadline.getDate())
    }

  }
  );
  setHighlightedDays(hDays)

};
const fetchProjects = async (setProjects: React.Dispatch<React.SetStateAction<ProjectDeadline[]>>) => {
  const header  = {
    "Authorization": "teacher2"
  }
  try{
    const response = await fetch(`${API_URL}/projects`, {
      headers:header
    })
    const jsonData = await response.json();
    let formattedData: ProjectDeadline[] = await Promise.all( jsonData.data.map(async (item:Project) => {
      const url_split = item.project_id.split('/')
      const project_id = url_split[url_split.length -1]
      const response_submissions = await (await fetch(encodeURI(`${API_URL}/submissions?project_id=${project_id}`), {
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
      const project_item = await (await fetch(encodeURI(`${API_URL}/projects/${project_id}`), {
        headers:header
      })).json()

      //fetch the course
      const response_courses = await (await fetch(encodeURI(`${API_URL}/courses/${project_item.data.course_id}`), {
        headers: header
      })).json()
      const course = {
        course_id: response_courses.data.course_id,
        name: response_courses.data.name,
        teacher: response_courses.data.teacher,
        ufora_id: response_courses.data.ufora_id
      }
      if(item.deadlines){
        return item.deadlines.map((d:string[]) => {
          return  {
            project_id: item.project_id,
            title: item.title,
            description: item.description,
            assignment_file: item.assignment_file,
            deadline: new Date(d[1]),
            deadline_description: d[0],
            course_id: Number(item.course_id),
            visible_for_students: Boolean(item.visible_for_students),
            archived: Boolean(item.archived),
            test_path: item.test_path,
            script_name: item.script_name,
            regex_expressions: item.regex_expressions,
            short_submission: latest_submission,
            course: course
          }
        })
      }
      // contains no dealine:
      return [{
        project_id: item.project_id,
        title: item.title,
        description: item.description,
        assignment_file: item.assignment_file,
        deadline: undefined,
        deadline_description: undefined,
        course_id: Number(item.course_id),
        visible_for_students: Boolean(item.visible_for_students),
        archived: Boolean(item.archived),
        test_path: item.test_path,
        script_name: item.script_name,
        regex_expressions: item.regex_expressions,
        short_submission: latest_submission,
        course: course
      }]
      
    }));
    formattedData = formattedData.flat()
    setProjects(formattedData);
    return formattedData
  } catch (e) {
    console.error("A server error occurred");
    return []
  }
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
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchProjects(setProjects).then(p => {
      handleMonthChange(initialValue, p,setHighlightedDays)
      setIsLoading(false)
    })
  }, []);

  // Update selectedDay state when a day is selected
  const handleDaySelect = (day: Dayjs) => {
    setSelectedDay(day);
  };
  const futureProjects = projects
    .filter((p) => (p.deadline && dayjs(dayjs()).isBefore(p.deadline)))
    .sort((a, b) => dayjs(a.deadline).diff(dayjs(b.deadline)))
    .slice(0, 3) // only show the first 3

  const pastDeadlines = projects
    .filter((p) => p.deadline && (dayjs()).isAfter(p.deadline))
    .sort((a, b) => dayjs(b.deadline).diff(dayjs(a.deadline)))
    .slice(0, 3) // only show the first 3
  const noDeadlineProject = projects.filter((p) => p.deadline === undefined)
  return (
    <Container style={{ paddingTop: '50px' }}>
      <Grid container spacing={2} wrap="nowrap">
        {isLoading ? (
          <Typography variant="body1">
            {t('loading')}
          </Typography>
        ): (
          <>
            <Grid item xs={6}>
              <Card>
                <CardContent>
                  <Typography variant="body1">
                    {t('myProjects')}
                  </Typography>
                  {futureProjects.length + noDeadlineProject.length > 0? (
                    <>
                      <ProjectDeadlineCard deadlines={futureProjects} />
                      <ProjectDeadlineCard deadlines={noDeadlineProject}/>
                    </>
                  ) : (
                    <Typography variant="body1">
                      {t('no_projects')}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={6}>
              <Card>

                <CardContent>
                  <Typography variant="body1">
                    {t('deadlines')}
                  </Typography>
                  {pastDeadlines.length > 0 ? (
                    <ProjectDeadlineCard deadlines={pastDeadlines} />
                  ) : (
                    <Typography variant="body1">
                      {t('no_projects')}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={6}>
              <Card>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                  <DateCalendar
                    value={selectedDay}
                    onMonthChange={(date: Dayjs) => { handleMonthChange(date, projects, setHighlightedDays) }}
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
          </>
        )}
      </Grid>
    </Container>
  );
}