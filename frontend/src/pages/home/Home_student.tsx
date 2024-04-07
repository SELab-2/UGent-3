import { useTranslation } from "react-i18next";
import {Card, CardContent, Typography, Grid, Container, Badge, Box} from '@mui/material';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import {DayCalendarSkeleton, LocalizationProvider} from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { CardActionArea } from '@mui/material';
import {Link } from "react-router-dom";

import React, {useEffect, useState} from 'react';
import dayjs, {Dayjs} from "dayjs";
import { PickersDay, PickersDayProps } from '@mui/x-date-pickers/PickersDay';

interface ShortSubmission {
  submission_id:number,
  submission_time:Date,
  submission_status:string
}
interface Project {
  project_id:number ,
  title :string,
  description:string,
  assignment_file:string,
  deadline:Date,
  course_id:number,
  visible_for_students:boolean,
  archived:boolean,
  test_path:string,
  script_name:string,
  regex_expressions:string[],
  short_submission: ShortSubmission

}
interface Course {
  course_id: string;
  name: string;
  teacher: string;
  ufora_id: string;
}
const apiUrl = import.meta.env.VITE_APP_API_URL
const initialValue = dayjs(Date.now());

interface DeadlineInfoProps {
  selectedDay: Dayjs;
  deadlines: Project[];
}
interface ProjectCardProps{
  deadlines:Project[]
}

const DeadlineInfo: React.FC<DeadlineInfoProps> = ({ selectedDay, deadlines }) => {
  const { t } = useTranslation('translation', { keyPrefix: 'student' });
  const deadlinesOnSelectedDay = deadlines.filter(
    deadline => dayjs(deadline.deadline).isSame(selectedDay, 'day')
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
      ) : <ProjectCard deadlines={deadlinesOnSelectedDay}/>}
    </div>
  );
};
const ProjectCard: React.FC<ProjectCardProps> = ({  deadlines }) => {
  const { t } = useTranslation('translation', { keyPrefix: 'student' });
  //list of the corresponding assignment
  return (
    <Box>
      {deadlines.map((project, index) => (
        <Card key={index} style={{margin: '10px 0'}}>
          <CardActionArea component={Link} to={`/submission/${project.short_submission.submission_id}`}>
            <CardContent>
              <Typography variant="h6" style={{color: project.short_submission.submission_status === 'SUCCESS' ? 'green' : 'red'}}>
                {project.title}
              </Typography>
              <Typography variant="subtitle1">
                {t('course')}: {"placeholder name"}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {t('last_submission')}: {project.short_submission.submission_status}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Deadline: {dayjs(project.deadline).format('MMMM D, YYYY')}
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      ))}

    </Box>
  );
};

/**
 *
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
const changeMonth = (
  date:Dayjs, 
  projects:Project[], 
  setHighlightedDays:React.Dispatch<React.SetStateAction<number[]>>,
) =>{
  const month = date.month()
  const year = date.year()
  const hDays:number[] = []
  projects.map((project, ) => {
    if(project.deadline.getMonth() == month && project.deadline.getFullYear() == year){
      hDays.push(project.deadline.getDate())
    }
  }
  );
  setHighlightedDays(hDays)
}
const handleMonthChange =(
  date: Dayjs,
  projects:Project[],
  setHighlightedDays: React.Dispatch<React.SetStateAction<number[]>>,
) => {

  setHighlightedDays([]);
  // projects are now only fetched on page load
  changeMonth(date, projects, setHighlightedDays)

};
const fetchProjects = async (setProjects: React.Dispatch<React.SetStateAction<Project[]>>) => {
  const response = await fetch(`${apiUrl}/projects`, {
    headers: {
      "Authorization": "teacher2" // todo add true authorization
    },
  })
  const jsonData = await response.json();
  const formattedData: Project[] = await Promise.all( jsonData.data.map(async (item:Project) => {
    const uid:string = "Bart" // todo check if we can fecth it so and get the uid of the logged in user
    const project_id:number = 94 // todo make this item.project_id when fixed
    const response_submissions = await (await fetch(encodeURI(`${apiUrl}/submissions?&project_id=${project_id}`), {
      headers: {
        "Authorization": "teacher2" // todo add true authorization
      },
    })).json()
    //get the latest submission
    const latest_submission = response_submissions.data.map((submission:ShortSubmission) => ({
      submission_id: submission.submission_id,//todo convert this into a number after bugfix
      submission_time: new Date(submission.submission_time),
      submission_status: submission.submission_status
    }
    )).sort((a:ShortSubmission, b:ShortSubmission) => b.submission_time.getTime() - a.submission_time.getTime())[0];
    return  {
      project_id: item.project_id, // todo convert this into a number after bug fix "project_id"
      title: item.title,
      description: item.description,
      assignment_file: item.assignment_file,
      deadline: new Date(item.deadline),
      course_id: Number(item.course_id),
      visible_for_students: Boolean(item.visible_for_students),
      archived: Boolean(item.archived),
      test_path: item.test_path,
      script_name: item.script_name,
      regex_expressions: item.regex_expressions,
      short_submission: latest_submission
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

  const [projects, setProjects] = useState<Project[]>([]);

  const [highlightedDays, setHighlightedDays] = React.useState<number[]>([]);

  useEffect(() => {
    fetchProjects(setProjects).then(p => {
      handleMonthChange(initialValue, p,setHighlightedDays)
    })
  }, []);

  const [selectedDay, setSelectedDay] = useState<Dayjs>(dayjs(Date.now()));

  // Update selectedDay state when a day is selected
  const handleDaySelect = (day: Dayjs) => {
    setSelectedDay(day);
    
  };

  return (
    <Container style={{ paddingTop: '50px' }}>
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Typography variant="body2">
            {t('myProjects')}
          </Typography>

          <ProjectCard deadlines={projects
            .filter((project) => dayjs(dayjs()).isBefore(project.deadline))
            .sort((a, b) => dayjs(a.deadline).isBefore(dayjs(b.deadline)) ? -1 : 1)
            .slice(0, 3)
          } />

        </Grid>
        <Grid item xs={6}>
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
                } as any,
              }}
            />
          </LocalizationProvider>
        </Grid>
        <Grid item xs={6}>
          <Typography variant="body2">
            {t('deadlines')}
          </Typography>
          <ProjectCard deadlines={projects
            .filter((project) => dayjs(dayjs()).isAfter(project.deadline))
            .sort((a, b) => dayjs(a.deadline).isAfter(dayjs(b.deadline)) ? -1 : 1)
            .slice(-2)
          } />
        </Grid>
        <Grid item xs ={6}>
          <Typography variant="body2">
            {t('deadlinesOnDay')} {selectedDay.format('MMMM D, YYYY')}
          </Typography>
          <DeadlineInfo selectedDay={selectedDay} deadlines={projects} />
        </Grid>
      </Grid>
    </Container>
  );
}
