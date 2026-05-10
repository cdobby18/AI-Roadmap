import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueOut, IssueUpdate, IssuesStatus
from app.storage import load_data, save_data

# Router for issue-related endpoints
router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

# Get all issues
@router.get("/", response_model=list[IssueOut])
def get_issues():
    """Return all issues"""
    issues = load_data()
    return issues

# Create a new issue
@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    """Create Issue"""
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

# Get a single issue by ID
@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str):
    """Retrieve specific issue by id"""
    issues = load_data()

    for issue in issues:
        if issue["id"] == issue_id:
            return issue

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue Not Found"
    )

# Update an existing issue
@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: str, payload: IssueUpdate):
    """Update existing issue"""
    issues = load_data()

    for index, issue in enumerate(issues):
        if issue["id"] == issue_id:

            # Copy existing issue
            updated_issue = issue.copy()

            # Update only provided fields
            if payload.title is not None:
                updated_issue["title"] = payload.title

            if payload.description is not None:
                updated_issue["description"] = payload.description

            if payload.priority is not None:
                updated_issue["priority"] = payload.priority

            if payload.status is not None:
                updated_issue["status"] = payload.status

            # Replace old issue with updated one
            issues[index] = updated_issue

            save_data(issues)
            return updated_issue

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue Not Found"
    )

# Delete an issue by ID
@router.delete("/{issue_id}", response_model=IssueOut)
def delete_issue(issue_id: str):
    """Delete issue by id"""
    issues = load_data()

    for index, issue in enumerate(issues):
        if issue["id"] == issue_id:

            # Remove issue from list
            deleted_issue = issues.pop(index)

            save_data(issues)
            return deleted_issue

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue Not Found"
    )