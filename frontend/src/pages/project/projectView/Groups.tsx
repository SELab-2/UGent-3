import { Box, Menu, MenuItem, Typography, Paper, Grid, IconButton, InputLabel, Input, Button } from "@mui/material";
import { ClearIcon } from "@mui/x-date-pickers";
import { useState, useCallback, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { apiHost } from "../../../components/Courses/CourseUtils";
import { authenticatedFetch } from "../../../utils/authenticated-fetch";

interface Group {
    group_id: string;
    size: number;
}

export function GroupMenuHolder(){
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const openGroupMenu = Boolean(anchorEl);
    
  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
    
  const handleClose = () => {
    setAnchorEl(null);
  };
    
  return (
    <>
      <Button onClick={handleClick}>Groups</Button>
      <GroupMenu projectId={"1"} open={openGroupMenu} handleClose={handleClose} anchorEl={anchorEl} />
    </>
  );
}

/**
 * @param projectId - Id of the project
 * @param open - Boolean to check if the menu is open
 * @param handleClose - Function to close the menu
 * @param anchorEl - Element to anchor the menu
 * @returns Component to display group menu
 */
export function GroupMenu({projectId,open,handleClose, anchorEl}: {projectId:string, open: boolean, handleClose : () => void, anchorEl: HTMLElement | null}) {
  const { t } = useTranslation('translation', { keyPrefix: 'courseDetailTeacher' });
  
  const [groups, setGroups] = useState<Group[]>([]);
  const [size, setSize] = useState<number>(0);
    
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSize(Number(event.target.value));
  };

  const getGroups = useCallback(() => {
    authenticatedFetch(`${apiHost}/projects/${projectId}/groups`, {
      method: 'GET',
    })
      .then(response => response.json())
      .then(data => {
        setGroups(data.data);
      })
  }, [projectId]);
  
  const handleNewGroup = () => {
    const bodyContent: { size: number } = { "size": size };
  
    authenticatedFetch(`${apiHost}/projects/${projectId}/groups`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bodyContent)
    })
      .then(() => getGroups())
  }
  
  const handleDeleteGroup = (groupId: string) => {
    authenticatedFetch(`${apiHost}/projects/${projectId}/groups/${groupId}`,
      {
        method: 'DELETE'
      })
      .then(() => getGroups());
  }
  
  useEffect(() => {
    getGroups();
  }, [t, getGroups ]);
  
  return (
    <Box>
      <Menu 
        open={open} 
        onClose={handleClose} 
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
      >
        <MenuItem disabled>
          <Typography variant="h6">{t('joinCodes')}</Typography>
        </MenuItem>
        <Paper elevation={0} style={{margin:"1rem", width:"30vw" ,maxHeight: "20vh", height: "20vh", overflowY:"auto" }}>
          {groups.map((group:Group) => (
            <MenuItem key={group.group_id}>
              <Grid container direction={"row"}>
                <Grid width={"7vw"} marginRight={"1rem"} item>
                  <Typography variant="body1">{group.group_id}</Typography>
                </Grid>
                <Grid item width={"7vw"}>
                  <Typography variant="body1">{group.size}</Typography>
                </Grid>
                <Grid item>
                  <IconButton onClick={() => handleDeleteGroup(group.group_id)}>
                    <ClearIcon />
                  </IconButton>
                </Grid>
              </Grid>
            </MenuItem>
          ))}
        </Paper>
        <MenuItem style={{marginTop:"1rem"}}>
          <InputLabel htmlFor="size" style={{marginRight: '1rem'}}>{t('groupSize')}: </InputLabel>
          <Input
            id="size"
            type="number"
            value={size}
            onChange={handleInputChange}
            style={{marginRight:"2rem"}}
          />
          <Button onClick={handleNewGroup}>{t('newGroup')}</Button>
        </MenuItem>
      </Menu>
    </Box>
  );
}