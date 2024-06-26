import {CardActionArea, Card, CardContent, Link, Typography, Box, Button} from '@mui/material';
import { useTranslation } from "react-i18next";
import dayjs from "dayjs";
import {ProjectDeadline} from "./ProjectDeadline.tsx";
import React from "react";
import { useNavigate } from 'react-router-dom';
import i18next from 'i18next';

interface ProjectCardProps{
  deadlines:ProjectDeadline[],
  showCourse?:boolean
}

/**
 * A clickable display of a project deadline
 * @param deadlines - A list of all the deadlines
 * @param pred - A predicate to filter the deadlines
 * @returns Element
 */
export const ProjectDeadlineCard: React.FC<ProjectCardProps> = ({  deadlines, showCourse = true }) => {
  const { t } = useTranslation('translation', { keyPrefix: 'student' });
  const navigate = useNavigate();

  //list of the corresponding assignment
  return (
    <Box>
      {deadlines.map((project, index) => (
       
        <Card key={index} style={{margin: '10px 0'}}>
          <CardActionArea LinkComponent={Link} href={`/${i18next.resolvedLanguage}/projects/${project.project_id}`}>
            <CardContent>
              <Typography variant="h6" style={{color: project.short_submission ?
                (project.short_submission.submission_status === 'SUCCESS' ? 'green' : 
                  (project.short_submission.submission_status === 'RUNNING' ? '#686868' : 'red')
                ) : '#686868'}}>
                {project.title}
              </Typography>
              {showCourse && (
                <Typography variant="subtitle1">
                  {t('course')}:
                  <Button
                    style={{
                      color: 'inherit',
                      textTransform: 'none'
                    }}
                    onMouseDown={event => event.stopPropagation()}
                    onClick={(event) => {
                      event.stopPropagation(); // stops the event from reaching CardActionArea
                      event.preventDefault();
                      navigate(`/${i18next.resolvedLanguage}/courses/${project.course.course_id}`)
                    }}
                  >
                    {project.course.name}
                  </Button>
                </Typography>
              )}
              <Typography variant="body2" color="textSecondary">
                {t('last_submission')}: {project.short_submission ?
                  t(project.short_submission.submission_status.toString()) : t('no_submission_yet')}
              </Typography>
              {project.deadline && (
                <Typography variant="body2" color="textSecondary">
                  Deadline: {dayjs(project.deadline).format('MMMM D, YYYY')}
                </Typography>
              )}
              {project.short_submission?.grading && (
                <Typography variant="body2" align="right">
                  {project.short_submission.grading}/20
                </Typography>
              )}
            </CardContent>
          </CardActionArea>
        </Card>
      ))

      }
    </Box>
  );
};
