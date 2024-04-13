import {CardActionArea, Card, CardContent, Typography, Box, Button} from '@mui/material';
import {Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import dayjs from "dayjs";
import {ProjectDeadline, Deadline} from "./ProjectDeadline.tsx";
import React from "react";
import { useNavigate } from 'react-router-dom';

interface ProjectCardProps{
  deadlines:ProjectDeadline[],
  pred?: (deadline:Deadline) => boolean
}

/**
 * A clickable display of a project deadline
 * @param deadlines - A list of all the deadlines
 * @param pred - A predicate to filter the deadlines
 * @returns Element
 */
export const ProjectDeadlineCard: React.FC<ProjectCardProps> = ({  deadlines }) => {
  const { t } = useTranslation('translation', { keyPrefix: 'student' });
  const navigate = useNavigate();

  //list of the corresponding assignment
  return (
    <Box>
      {deadlines.map((project, index) => (
       
        <Card key={index} style={{margin: '10px 0'}}>
          <CardActionArea component={Link} to={`/${project.project_id}`}>
            <CardContent>
              <Typography variant="h6" style={{color: project.short_submission ?
                (project.short_submission.submission_status === 'SUCCESS' ? 'green' : 'red') : '#686868'}}>
                {project.title}
              </Typography>
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
                    navigate(`/courses/${project.course.course_id}`)
                  }}
                >
                  {project.course.name}
                </Button>
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {t('last_submission')}: {project.short_submission ?
                  t(project.short_submission.submission_status.toString()) : t('no_submission_yet')}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                  Deadline: {dayjs(project.deadline).format('MMMM D, YYYY')}
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      ))

      }
    </Box>
  );
};