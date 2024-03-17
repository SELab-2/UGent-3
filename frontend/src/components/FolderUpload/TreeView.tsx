import { Box, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import LazyTreeView from "./LazyTreeView";
import { FileIcon, defaultStyles } from "react-file-icon";
import { TreeNode } from "./types";

interface FileTreeViewProps {
  rootFolder: FileSystemDirectoryEntry | null;
  onFileSelect?: (file: FileSystemEntry) => void;
}

export default function FileTreeView({
  rootFolder,
  onFileSelect,
}: FileTreeViewProps): JSX.Element {
  const [expanded, setExpanded] = useState([] as string[]);
  const [data, setData] = useState<TreeNode[] | null>(null);
  useEffect(() => {
    if (rootFolder) {
      const directory = {
        key: rootFolder.fullPath,
        title: rootFolder.name,
        data: { fileObject: rootFolder },
      } as TreeNode;
      readDirectoryEntries(rootFolder).then((data) => {
        directory["children"] = data;
        setData([directory]);
      });
    }
  }, [rootFolder]);

  const handleToggle = (_event: any, nodeIds: string[]) => {
    setExpanded(nodeIds);
  };

  const handleSelect = (file: FileSystemEntry) => {
    onFileSelect && onFileSelect(file);
  };

  const lazyLoad = ({
    data,
  }: {
    key: string;
    children: TreeNode[] | undefined;
    data: Record<string, any>;
  }) => {
    return new Promise<TreeNode[]>((resolve) => {
      if (
        data["fileObject"] &&
        data["fileObject"].isDirectory &&
        !data.children
      ) {
        resolve(readDirectoryEntries(data["fileObject"]));
      }
      resolve([]);
    });
  };

  return (
    <Box>
      {data && (
        <LazyTreeView
          expanded={expanded}
          onNodeToggle={handleToggle}
          treeData={data}
          onFileSelect={handleSelect}
          titleRender={(node) => (
            <>
              {!node.data!["fileObject"].isDirectory ? (
                <Box display="flex">
                  <Box sx={{ width: "15px", height: "2px" }}>
                    <FileIcon
                      extension={getFileExtension(node.title)}
                      {...defaultStyles[getFileExtension(node.title)]}
                    />
                  </Box>

                  <Typography style={{ marginLeft: "0.5rem" }}>
                    {node.title}
                  </Typography>
                </Box>
              ) : (
                <> {node.title} </>
              )}
            </>
          )}
          lazyLoadFn={lazyLoad}
        />
      )}
    </Box>
  );
}

const readDirectoryEntries = (
  entry: FileSystemDirectoryEntry
): Promise<TreeNode[]> => {
  const reader = entry.createReader();

  const readEntries = (reader: FileSystemDirectoryReader) => {
    return new Promise<TreeNode[]>((resolve) => {
      let children: TreeNode[] = [];
      reader.readEntries((entries) => {
        entries.forEach(async (fileEntry) => {
          let child = {
            key: fileEntry.fullPath,
            title: fileEntry.name,
            data: { fileObject: fileEntry },
          } as TreeNode;
          if (fileEntry.isDirectory) {
            child["children"] = [];
          }
          children.push(child);
        });
        resolve(children);
      });
    });
  };

  try {
    return readEntries(reader);
  } catch (error) {
    throw new Error("Error reading directory entries");
  }
};

function getFileExtension(filename: string) {
  return filename.slice(((filename.lastIndexOf(".") - 1) >>> 0) + 2);
}
