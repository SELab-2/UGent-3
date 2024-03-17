// Based on https://github.com/bigrivi/mui-lazy-tree-view
import React, { useEffect, useState } from "react";
import {
  TreeView,
  TreeViewProps,
} from "@mui/x-tree-view/TreeView";
import equal from "fast-deep-equal";
import {
  TreeItemClasses,
  TreeItemContentProps,
  TreeItem as MuiTreeItem,
} from "@mui/x-tree-view/TreeItem";
import TreeItem from "./TreeItem";
import { TreeNode } from "./types";
import "./index.css";

const LAZY_LOAD__PLACEHOLDER = "_lazy_load_placeholder";

interface ITreeViewProps<Multiple extends boolean | undefined>
  extends TreeViewProps<Multiple> {
  treeData: TreeNode[];
  titleRender?: (node: TreeNode) => React.ReactNode;
  lazyLoadFn?: (args: {
    key: string;
    children: TreeNode[] | undefined;
    data: Record<string, any>;
  }) => Promise<TreeNode[]>;
  treeItemClasses?: Partial<TreeItemClasses>;
  ContentComponent?: React.JSXElementConstructor<TreeItemContentProps>;
  onFileSelect?: (file: FileSystemEntry) => void;
}


const LazyTreeView = <Multiple extends boolean | undefined = undefined>({
  treeData,
  lazyLoadFn,
  treeItemClasses,
  titleRender,
  ContentComponent,
  expanded: expandedProp,
  onNodeToggle: onNodeToggleProp,
  defaultCollapseIcon,
  defaultExpandIcon,
  onFileSelect,
  ...treeProps
}: ITreeViewProps<Multiple>) => {
  const [expanded, setExpanded] = useState(
    expandedProp ? [...expandedProp] : []
  );

  useEffect(() => {
    if (expandedProp) {
      if (!equal(expandedProp, expanded)) {
        setExpanded(expandedProp);
      }
    }
  }, [expandedProp]);

  const handleToggle = (
    event: React.SyntheticEvent<Element, Event>,
    nodeIds: string[]
  ) => {
    setExpanded(nodeIds);
    onNodeToggleProp && onNodeToggleProp(event, nodeIds);
  };

  const handleExpand = (key: string) => {
    const newExpanded = [...expanded, key];
    setExpanded(newExpanded);
    onNodeToggleProp && onNodeToggleProp(null, newExpanded);
  };

  const renderChildren = (
    parent: TreeNode | undefined,
    children: TreeNode[] | undefined
  ) => {
    const hasLazyLoad = typeof children != "undefined" && children.length == 0;

    if (hasLazyLoad && parent) {
      return (
        <MuiTreeItem nodeId={parent.key + LAZY_LOAD__PLACEHOLDER}></MuiTreeItem>
      );
    }
    if (!children) {
      return null;
    }

    return children.map((node) => {
      return (
          <TreeItem
            sx={{".MuiTreeView-root": {height: "50px"}}}
            key={node.key}
            node={node}
            collapseIcon={defaultCollapseIcon}
            expandIcon={defaultExpandIcon}
            ContentComponent={ContentComponent}
            treeItemClasses={treeItemClasses}
            onExpand={handleExpand}
            titleRender={titleRender}
            lazyLoadFn={lazyLoadFn}
            renderChildren={renderChildren}
            onFileSelect={onFileSelect}
          />
      );
    });
  };
  return (
    <TreeView expanded={expanded} onNodeToggle={handleToggle} {...treeProps}>
      {treeData && renderChildren(null, treeData)}
    </TreeView>
  );
};

export default LazyTreeView;
