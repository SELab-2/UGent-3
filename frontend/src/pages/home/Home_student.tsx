import { useTranslation } from "react-i18next";
import {Card, CardContent, Typography, Grid, Container, Badge} from '@mui/material';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import {DayCalendarSkeleton, LocalizationProvider} from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { CardActionArea } from '@mui/material';
import {Link } from "react-router-dom";

import React, { useState } from 'react';
import dayjs, {Dayjs} from "dayjs";
import { PickersDay, PickersDayProps } from '@mui/x-date-pickers/PickersDay';


function fakeFetch(date: Dayjs, { signal }: { signal: AbortSignal }) {
  return new Promise<{ daysToHighlight: number[] }>((resolve, reject) => {
    const timeout = setTimeout(() => {
      const daysInMonth = date.daysInMonth();
      const daysToHighlight: number[] = [5, 12, 15];

      resolve({ daysToHighlight });
    }, 500);

    signal.onabort = () => {
      clearTimeout(timeout);
      reject(new DOMException('aborted', 'AbortError'));
    };
  });
}
const initialValue = dayjs(Date.now());

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
          fontSize: '0.5em', // Adjust as needed
          top: 8, // Adjust as needed
          right: 8, // Adjust as needed
        },
      }}
    >
      <PickersDay {...other} outsideCurrentMonth={outsideCurrentMonth} day={day} />
    </Badge>
  );
}

/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function HomeStudent() {
  const list_of_projects = [
    {"deadline": "2024-05-01", "title": "Python lists", "course_id":"123", "project_id": "111"},
    {"deadline": "2024-06-05", "title": "Prolog intro", "course_id":"333", "project_id": "222"},
    {"deadline": "2024-04-01", "title": "Verlopen", "course_id":"333", "project_id": "222"}
  ]
  // get the corresponding course and latest submission, order is important needs to be the same for matching
  const latest_submissions = [{"project_id": "111", "submission_status": "FAIL",
    "submission_id":"111"},
  {"project_id": "333", "submission_status": "SUCCESS", "submission_id": "232"},
  {"project_id": "333", "submission_status": "SUCCESS", "submission_id": "444"}

  ]
  const courses = [{"course_id": "123", "name": "Programmeren"},
    {"course_id": "222", "name": "LOGPROG"},
    {"course_id": "222", "name": "FUNPROG"}
  ]
  const { t } = useTranslation();
  //const [value, setValue] = useState<Date | null>(new Date());
  /*useEffect(() => {
    fetch("http://172.17.0.2:5000/project?uid=123")
      .then(response => response.json())
  }, []);*/
  const requestAbortController = React.useRef<AbortController | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [highlightedDays, setHighlightedDays] = React.useState<number[]>([]);
  const fetchHighlightedDays = (date: Dayjs) => {
    const controller = new AbortController();

    fakeFetch(date, {
      signal: controller.signal,
    })
      .then(({ daysToHighlight }) => {
        setHighlightedDays(daysToHighlight);
        setIsLoading(false);
      })
      .catch((error) => {
        // ignore the error if it's caused by `controller.abort`
        if (error.name !== 'AbortError') {
          throw error;
        }
      });

    requestAbortController.current = controller;
  };

  React.useEffect(() => {
    fetchHighlightedDays(initialValue);
    // abort request on unmount
    return () => requestAbortController.current?.abort();
  }, []);

  const handleMonthChange = (date: Dayjs) => {
    if (requestAbortController.current) {
      // make sure that you are aborting useless requests
      // because it is possible to switch between months pretty quickly
      requestAbortController.current.abort();
    }

    setIsLoading(true);
    setHighlightedDays([]);
    fetchHighlightedDays(date);
  };
  const [selectedDay, setSelectedDay] = useState<Dayjs | null>(null);

  // Update selectedDay state when a day is selected
  const handleDaySelect = (day: Dayjs) => {
    console.log(day.get('day'));
    setSelectedDay(day);
  };

  return (
    <Container style={{ paddingTop: '50px' }}>
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Typography variant="body2">
            {t('myProjects')}
          </Typography>
          {latest_submissions.map((submission, index) => (
            (new Date(list_of_projects[index].deadline).getTime() > Date.now())  && (
              <Card key={index} style={{margin: '10px 0'}}>
                <CardActionArea component={Link} to={`/submission/${submission.submission_id}`}>
                  <CardContent>
                    <Typography variant="h6" style={{color: submission.submission_status === 'SUCCESS' ? 'green' : 'red'}}>
                      {list_of_projects[index].title}
                    </Typography>
                    <Typography variant="subtitle1">
                      {t('course')}: {courses[index].name}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {t('last_submission')}: {submission.submission_status}
                    </Typography>
                  </CardContent>
                </CardActionArea>

              </Card>
            )
        
          ))}
        </Grid>
        <Grid item xs={6}>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DateCalendar
              defaultValue={initialValue}
              loading={isLoading}
              onMonthChange={handleMonthChange}
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
          {latest_submissions.map((submission, index) => (
            (new Date(list_of_projects[index].deadline).getTime() <= Date.now())  && (
              <Card key={index} style={{margin: '10px 0'}}>
                <CardActionArea component={Link} to={`/submission/${submission.submission_id}`}>
                  <CardContent>
                    <Typography variant="h6" style={{color: submission.submission_status === 'SUCCESS' ? 'green' : 'red'}}>
                      {list_of_projects[index].title}
                    </Typography>
                    <Typography variant="subtitle1">
                      {t('course')}: {courses[index].name}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {t('last_submission')}: {submission.submission_status}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            )
          ))}
        </Grid>
      </Grid>
    </Container>
  );
}
