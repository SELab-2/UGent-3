import { Box, Grid, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import FileTreeView from "./TreeView";
import hljs from "highlight.js";
import SyntaxHighlighter from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

interface FolderDragDropProps {
  onFolderDrop: (folder: FileSystemEntry) => void;
  onFileDrop: (file: FileSystemEntry) => void;
}

const FolderDragDrop: React.FC<FolderDragDropProps> = ({
  onFolderDrop,
  onFileDrop,
}) => {
  const [isDraggingOver, setIsDraggingOver] = useState(false);
  const [fileRawText, setFileRawText] = useState<string>("");
  const [selectedFile, setSelectedFile] = useState<FileSystemEntry | null>(
    null
  );
  const [rootFolder, setRootFolder] = useState<FileSystemDirectoryEntry | null>(
    null
  );

  useEffect(() => {
    if (selectedFile) {
      readTextFromFile(selectedFile as FileSystemFileEntry).then((text) => {
        if (text) {
          console.log(
            hljs.getLanguage(getFileExtension(selectedFile?.name))?.name
          );
          setFileRawText(text);
        }
      });
    }
  }, [selectedFile]);

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDraggingOver(true);
  };

  const handleDragLeave = () => {
    setIsDraggingOver(false);
  };

  const handleDrop = async (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDraggingOver(false);

    const items = event.dataTransfer?.items;
    if (items) {
      console.log(items);
      const folderItem = items[0];
      if (folderItem.kind === "file") {
        const entry = folderItem.webkitGetAsEntry();
        if (entry && entry.isFile) {
          onFileDrop(entry);
        }
        if (entry && entry.isDirectory) {
          setRootFolder(entry as FileSystemDirectoryEntry);
        }
      }
    }
  };

  return (
    <Grid container direction="column" style={{margin: "1rem"}} spacing={2}>
      <Grid item>
        <Box
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          style={{ borderColor: isDraggingOver ? "#ff5722" : "#ccc" }}
        >
          <Typography variant="h5">Drag & Drop a Folder Here</Typography>
        </Box>
      </Grid>
      <Grid item>
        <Grid container spacing="20">
          <Grid item sx={{ width: "40rem" }}>
            <FileTreeView
              rootFolder={rootFolder}
              onFileSelect={setSelectedFile}
            />
          </Grid>
          <Grid item>
            {selectedFile?.name && (
              <SyntaxHighlighter
                customStyle={{width: "40rem", height: "20rem", overflow: "auto", margin: "0rem"}}
                language={hljs
                  .getLanguage(getFileExtension(selectedFile?.name))
                  ?.name?.toLowerCase()}
                style={docco}
              >
                {fileRawText || "No file selected."}
              </SyntaxHighlighter>
            )}
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

async function readTextFromFile(
  entry: FileSystemFileEntry
): Promise<string | null> {
  // Check if the entry is a file
  if (entry.isFile) {
    try {
      // Get a file object
      const file = await new Promise<File>((resolve, reject) => {
        entry.file(resolve, reject);
      });

      // Read the file as text
      const text = await file.text();

      // Return the raw text
      return text;
    } catch (error) {
      console.error("Error reading file:", error);
      return null;
    }
  } else {
    console.error("Entry is not a file.");
    return null;
  }
}

function getFileExtension(filename: string) {
  return filename.slice(((filename.lastIndexOf(".") - 1) >>> 0) + 2);
}

export default FolderDragDrop;
