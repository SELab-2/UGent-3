import { Button, Grid, Paper, Typography, styled } from "@mui/material";
import { verifyZipContents, getFileExtension } from "../../utils/file-utils";
import JSZip from "jszip";
import React, { useState } from "react";

interface FolderDragDropProps {
  onFileDrop?: (file: File) => void;
  regexRequirements?: string[];
  onWrongInput?: (message: string) => void;
}

const supportedFileTypes = ["application/x-zip-compressed", "application/zip"];

const FolderDragDrop: React.FC<FolderDragDropProps> = ({
  onFileDrop,
  regexRequirements,
  onWrongInput,
}) => {
  const [isDraggingOver, setIsDraggingOver] = useState(false);

  const VisuallyHiddenInput = styled("input")({
    clip: "rect(0 0 0 0)",
    clipPath: "inset(50%)",
    height: 1,
    overflow: "hidden",
    position: "absolute",
    bottom: 0,
    left: 0,
    whiteSpace: "nowrap",
    width: 1,
  });

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDraggingOver(true);
  };

  const handleDragLeave = () => {
    setIsDraggingOver(false);
  };

  const handleNewFile = async (entry: File) => {
    if (onFileDrop && supportedFileTypes.includes(entry.type)) {
      const fileName: string = entry.name;
      const fileExtension: string = getFileExtension(fileName);
      if (fileExtension === "zip" && regexRequirements) {
        try {
          const regexReport = await JSZip.loadAsync(entry).then((zip) => {
            return verifyZipContents(zip, regexRequirements);
          });
          if (regexReport.isValid) {
            onFileDrop(entry);
          } else {
            onWrongInput &&
              onWrongInput(
                `Missing required fields: ${regexReport.missingFiles.join(
                  ", "
                )}.`
              );
          }
        } catch {
          onWrongInput &&
            onWrongInput("Something went wrong getting parsing your zip.");
        }
      } else {
        onFileDrop(entry);
      }
    } else {
      onWrongInput && onWrongInput("The file must be zipped.");
    }
  };

  const handleDrop = async (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDraggingOver(false);

    const items = event.dataTransfer?.items;
    if (items && onFileDrop) {
      const folderItem = items[0];
      if (folderItem.kind === "file") {
        const entry = folderItem.getAsFile();
        if (entry) {
          handleNewFile(entry);
        } else {
          onWrongInput &&
            onWrongInput("Something went wrong getting your file.");
        }
      } else {
        onWrongInput && onWrongInput("Your input must be a file.");
      }
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleNewFile(file);
    }
  }

  return (
    <Grid container direction="column" style={{ margin: "1rem" }} spacing={2}>
      <Grid item>
        <Paper
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          style={{
            width: "fit-content",
            padding: "1rem",
            borderStyle: "dashed",
            backgroundColor: isDraggingOver ? "lightgray" : "inherit",
            textAlign: "center"
          }}
        >
          <Typography variant="h5">Drag & Drop a File Here</Typography>
          <Button
            component="label"
            role={undefined}
            tabIndex={-1}
          >
            <Typography>Or click to select a file</Typography>
            <VisuallyHiddenInput type="file" onChange={handleFileUpload} />
          </Button>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default FolderDragDrop;
