import { useTranslation } from "react-i18next";
import {Card, CardContent, Typography, Grid, Container, Badge} from '@mui/material';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import {DayCalendarSkeleton, LocalizationProvider} from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import React, {useEffect, useState} from 'react';
import dayjs, {Dayjs} from "dayjs";
import { PickersDay, PickersDayProps } from '@mui/x-date-pickers/PickersDay';
import {ProjectDeadlineCard} from "../project/projectDeadline/ProjectDeadlineCard.tsx";
import {ProjectDeadline} from "../project/projectDeadline/ProjectDeadline.tsx";
import {fetchProjects} from "../project/fetchProjects.tsx";
import {Title} from "../../components/Header/Title.tsx";

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
    project => (dayjs(project.deadline).isSame(selectedDay, 'day'))
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
    if(project.deadline.getMonth() == date.month() && project.deadline.getFullYear() == date.year()){
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
      <Title title={"Home"}/>
      <Grid container spacing={2} wrap="nowrap">
        <Grid item xs={6}>
          <Typography variant="body2">
            {t('myProjects')}
          </Typography>

          <ProjectDeadlineCard
            deadlines={projects
              .filter((p) => (dayjs(dayjs()).isBefore(p.deadline)))
              .sort((a, b) => dayjs(a.deadline).diff(dayjs(b.deadline)))
              .slice(0, 3) // only show the first 3
            } />

        </Grid>
        <Grid item xs={6}>
          <Typography variant="body2">
            {t('deadlines')}
          </Typography>
          <ProjectDeadlineCard
            deadlines={projects
              .filter((p) => dayjs(dayjs()).isAfter(p.deadline))
              .sort((a, b) => dayjs(b.deadline).diff(dayjs(a.deadline)))
              .slice(0, 3) // only show the first 3
            } />
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
