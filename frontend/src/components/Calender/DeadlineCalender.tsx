import {
  DateCalendar,
  LocalizationProvider,
  PickersDay,
  PickersDayProps,
  TimeField,
} from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs, { Dayjs } from "dayjs";
import { Deadline } from "../../types/deadline";
import {
  Badge,
  Box,
  Divider,
  Grid,
  IconButton,
  List,
  ListItem,
  Menu,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import SendIcon from "@mui/icons-material/Send";
import ClearIcon from "@mui/icons-material/Clear";
import { useTranslation } from "react-i18next";

interface DeadlineCalenderProps {
  deadlines: Deadline[];
  onChange: (deadline: Deadline[]) => void;
}

/**
 *
 * @param params - The deadlines and the onChange function
 * @returns - The DeadlineCalender component that displays the deadlines
 */
export default function DeadlineCalender({
  deadlines,
  onChange,
}: DeadlineCalenderProps) {
  const [deadlinesS, setDeadlines] = useState<Deadline[]>(deadlines);
  const { i18n } = useTranslation();

  const handleNewDeadline = (deadline: Deadline) => {
    const newDeadlines = [...deadlinesS, deadline];
    setDeadlines(newDeadlines);
    onChange(newDeadlines);
  };

  const handleDeadlineRemoved = (deadline: Deadline) => {
    const newDeadlines = deadlinesS.filter((d) => d !== deadline);
    setDeadlines(newDeadlines);
    onChange(newDeadlines);
  };

  return (
    <LocalizationProvider
      dateAdapter={AdapterDayjs}
      adapterLocale={i18n.language}
    >
      <DateCalendar
        slots={{ day: DeadlineDay }}
        slotProps={{
          day: {
            deadlines: deadlinesS,
            handleNewDeadline,
            handleDeadlineRemoved,
          } as any // eslint-disable-line @typescript-eslint/no-explicit-any,
        }}
      />
    </LocalizationProvider>
  );
}

/**
 *
 * @param props - The day and the deadlines
 * @returns - The DeadlineDay component that displays the deadlines for a specific day
 */
function DeadlineDay(
  props: PickersDayProps<Dayjs> & {
    deadlines?: Deadline[];
    editable?: boolean;
    handleNewDeadline?: (deadline: Deadline) => void;
    handleDeadlineRemoved?: (deadline: Deadline) => void;
  }
) {
  const {
    deadlines = [],
    day,
    outsideCurrentMonth,
    editable = false,
    handleNewDeadline,
    handleDeadlineRemoved,
    ...other
  } = props;
  const [descriptionMenuAnchor, setDescriptionMenuAnchor] =
    useState<null | HTMLElement>(null);

  const handleDescriptionMenu = (event: React.MouseEvent<HTMLElement>) => {
    setDescriptionMenuAnchor(event.currentTarget);
  };

  const handleCloseDescriptionMenu = () => {
    setDescriptionMenuAnchor(null);
  };

  const isDeadline =
    !outsideCurrentMonth &&
    deadlines.filter((deadline) => {
      return dayjs(deadline.deadline).isSame(day, "day");
    }).length > 0;

  return (
    <Badge
      badgeContent={isDeadline ? "🔵" : undefined}
      key={day.toString()}
      overlap="circular"
    >
      <PickersDay
        {...other}
        onClick={handleDescriptionMenu}
        day={day}
        outsideCurrentMonth={outsideCurrentMonth}
      />
      {(isDeadline || editable) && (
        <Menu
          anchorEl={descriptionMenuAnchor}
          open={Boolean(descriptionMenuAnchor)}
          onClose={handleCloseDescriptionMenu}
        >
          <DeadlineDescriptionMenu
            deadlines={deadlines}
            day={day}
            editable={editable}
            onNewDeadline={handleNewDeadline}
            onDeadlineRemoved={handleDeadlineRemoved}
          />
        </Menu>
      )}
    </Badge>
  );
}

/**
 *
 * @param params - The deadlines, the day, editable, onNewDeadline and onDeadlineRemoved functions
 * @returns - The DeadlineDescriptionMenu component that displays the deadlines for a specific day
 */
function DeadlineDescriptionMenu({
  deadlines,
  day,
  editable,
  onNewDeadline,
  onDeadlineRemoved,
}: {
  deadlines: Deadline[];
  day: Dayjs;
  editable: boolean;
  onNewDeadline?: (deadline: Deadline) => void;
  onDeadlineRemoved?: (deadline: Deadline) => void;
}) {
  const [description, setDescription] = useState<string>("");
  const [time, setTime] = useState<Dayjs | null>(null);

  const handleNewDeadline = () => {
    if (time && onNewDeadline && description.length > 0) {
      let newDeadline = day.clone();
      newDeadline = newDeadline.hour(time.hour());
      newDeadline = newDeadline.minute(time.minute());
      console.log(newDeadline.isSame(day, "day"));
      onNewDeadline({ deadline: newDeadline.toString(), description });
    }
    setDescription("");
    setTime(null);
  };

  const handleDeadlineRemoved = (deadline: Deadline) => {
    if (onDeadlineRemoved) {
      onDeadlineRemoved(deadline);
    }
  };

  return (
    <Grid container direction="column" gap="1rem" width="20vw">
      <Grid item>
        <List>
          {deadlines
            .filter((deadline) => {
              return dayjs(deadline.deadline).isSame(day, "day");
            })
            .map((deadline, index) => {
              return (
                <div key={index}>
                  <ListItem>
                    {deadline.description}
                    <Box flexGrow={1} />
                    <Typography>
                      {dayjs(deadline.deadline).format("HH:mm")}
                    </Typography>
                    {editable && (
                      <IconButton
                        onClick={() => handleDeadlineRemoved(deadline)}
                      >
                        <ClearIcon />
                      </IconButton>
                    )}
                  </ListItem>
                  <Divider />
                </div>
              );
            })}
        </List>
      </Grid>
      {editable && (
        <Grid item marginLeft="1rem">
          <Grid container spacing="1rem">
            <Grid item>
              <TextField
                id="new-discription-field"
                variant="outlined"
                size="small"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
              />
            </Grid>
            <Grid item sm={3.3}>
              <TimeField
                format="HH:mm"
                size="small"
                value={time}
                onChange={(newValue) => {
                  setTime(newValue);
                }}
              />
            </Grid>
            <Grid item>
              <IconButton onClick={handleNewDeadline}>
                <SendIcon />
              </IconButton>
            </Grid>
          </Grid>
        </Grid>
      )}
    </Grid>
  );
}
