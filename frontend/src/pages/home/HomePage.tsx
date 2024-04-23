import { useTranslation } from "react-i18next";
import {Card, CardContent, Typography, Grid, Container, Badge} from '@mui/material';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import {DayCalendarSkeleton, LocalizationProvider} from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import React, {useState} from 'react';
import dayjs, {Dayjs} from "dayjs";
import { PickersDay, PickersDayProps } from '@mui/x-date-pickers/PickersDay';
import {ProjectDeadlineCard} from "../project/projectDeadline/ProjectDeadlineCard.tsx";
import {ProjectDeadline} from "../project/projectDeadline/ProjectDeadline.tsx";
import {useLoaderData} from "react-router-dom";
import {Me} from "../../types/me.ts";

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

/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function HomePage() {
  const { t } = useTranslation('translation', { keyPrefix: 'student' });

  const [highlightedDays, setHighlightedDays] = React.useState<number[]>([]);

  const [selectedDay, setSelectedDay] = useState<Dayjs>(dayjs(Date.now()));
  const loader = useLoaderData() as {
    projects: ProjectDeadline[],
    me: Me
  }
  const projects = loader.projects

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

      </Grid>
    </Container>
  );
}
