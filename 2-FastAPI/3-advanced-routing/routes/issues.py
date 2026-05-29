"""
Issue management routes.
Demonstrates modular routing with APIRouter.
"""

import uuid
from fastapi import APIRouter, HTTPException, status
from schemas import IssueCreate, IssueOut, IssueUpdate, IssuesStatus
from storage import load_data, save_data

# Router for issue-related endpoints
router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


# ================================
# CRUD ENDPOINTS
# ================================

@router.get("/", response_model=list[IssueOut])
def get_issues():
    """Return all issues"""
    issues = load_data()
    return issues


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    """Create a new issue"""
    issues = load_data()

    new_issue = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority,
        "status": IssuesStatus.open,
    }

    issues.append(new_issue)
    save_data(issues)
    return new_issue


@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str):
    """Retrieve a specific issue by ID"""
    issues = load_data()

    for issue in issues:
        if issue["id"] == issue_id:
            return issue

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue Not Found"
    )


@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: str, payload: IssueUpdate):
    """Update an existing issue"""
    issues = load_data()

    for issue in issues:
        if issue["id"] == issue_id:
            update_data = payload.dict(exclude_unset=True)
            updated_issue = {**issue, **update_data}
            
            index = issues.index(issue)
            issues[index] = updated_issue
            save_data(issues)
            return updated_issue

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue Not Found"
    )


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: str):
    """Delete an issue"""
    issues = load_data()

    for i, issue in enumerate(issues):
        if issue["id"] == issue_id:
            issues.pop(i)
            save_data(issues)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue Not Found"
    )
