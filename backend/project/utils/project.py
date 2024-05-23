"""Utility functions for the project model"""

from typing import Tuple
from sqlalchemy.orm import Session
from project.models.project import Project

def is_valid_project(session: Session, project_id: any) -> Tuple[bool, str]:
    """Check if a project_id is valid

    Args:
        project_id (any): The project_id

    Returns:
        bool: Is valid
    """
    if project_id is None:
        return False, "The project_id is missing"

    if isinstance(project_id, str) and project_id.isdigit():
        project_id = int(project_id)
    elif not isinstance(project_id, int):
        return False, f"Invalid project_id typing (project_id={project_id})"

    project = session.get(Project, project_id)
    if project is None:
        return False, f"Invalid project (project_id={project_id})"
    return True, "Valid project"
