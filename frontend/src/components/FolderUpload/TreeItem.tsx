// Based on https://github.com/bigrivi/mui-lazy-tree-view

import React, { useEffect, useRef, useState } from "react";

import {
    TreeItem as MuiTreeItem,
    TreeItemContentProps,
    TreeItemProps as MuiTreeItemProps,
    TreeItemClasses
} from "@mui/x-tree-view/TreeItem";
import CustomContent from "./CustomContent";
import TreeItemLabel from "./Label";
import equal from "fast-deep-equal";
import { TreeNode } from "./types";

interface TreeItemsProps extends Omit<MuiTreeItemProps, "nodeId"> {
    node: TreeNode;
    treeItemClasses?: Partial<TreeItemClasses>;
    titleRender?: (node: TreeNode) => React.ReactNode;
    lazyLoadFn?: (args: {
        key: string;
        children: TreeNode[] | undefined;
        data: Record<string, any>;
    }) => Promise<any[]>;
    renderChildren: (
        parentNode: TreeNode,
        children: TreeNode[] | undefined
    ) => React.ReactNode;
    onExpand: (nodeKey: string) => void;
    ContentComponent?: React.JSXElementConstructor<TreeItemContentProps>;
    collapseIcon?: React.ReactNode;
    expandIcon?: React.ReactNode;
    onFileSelect?: (file: FileSystemEntry) => void;
}

const TreeItem = ({
    node,
    titleRender,
    lazyLoadFn,
    renderChildren,
    onExpand,
    treeItemClasses,
    ContentComponent,
    collapseIcon,
    expandIcon,
    onFileSelect,
    ...rest
}: TreeItemsProps) => {
    const [children, setChildren] = useState<TreeNode[] | undefined>(node.children);
    const isMountRef = useRef(false);
    const [loading, setLoading] = useState(false);

    const handleLazyLoad = async () => {
        setLoading(true);
        if(!lazyLoadFn) return;
        const nodes = await lazyLoadFn({
            key: node.key,
            children: node.children,
            data: node.data
        });
        node.children = nodes;
        setChildren(nodes);
        onExpand(node.key);
        setLoading(false);
    };

    const handleClick = async () => {
        if(node.data!["fileObject"].isFile){
            onFileSelect && onFileSelect(node.data!["fileObject"]);
        }
        else{
            await handleLazyLoad()
        };
    };

    useEffect(() => {
        if (isMountRef.current) {
            if (node.children != children) {
                if (!equal(node.children, children)) {
                    setChildren(node.children);
                }
            }
        }
    }, [node.children]);

    useEffect(() => {
        isMountRef.current = true;
        return () => {
            isMountRef.current = false;
        };
    }, []);
    return (
        <MuiTreeItem
            ContentComponent={ContentComponent ?? CustomContent}
            key={node.key}
            nodeId={node.key}
            disabled={node.disabled}
            {...rest}
            classes={treeItemClasses}
            onClick={handleClick}
            label={
                <TreeItemLabel
                    loading={loading}
                    titleRender={titleRender}
                    onLazyLoad={handleLazyLoad}
                    collapseIcon={collapseIcon}
                    expandIcon={expandIcon}
                    node={node}
                />
            }
        >
            {renderChildren(node, children)}
        </MuiTreeItem>
    );
};

export default TreeItem;