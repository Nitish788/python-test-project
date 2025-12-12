# Constants Guide

## 🎯 Overview

This project uses a centralized constants file (`app/constants.py`) to define all application-level constants. This follows Python conventions and the pattern specified for module-level constants extraction (UPPER_CASE).

## 📋 Why Use Constants?

1. **Single Source of Truth** - Change a value in one place
2. **Avoid Magic Numbers** - Self-documenting code
3. **Type Safety** - Type hints for all constants
4. **Easy Maintenance** - Find all uses of a constant
5. **Consistency** - Ensures uniform values across the app

## 📁 Structure

### Status Constants

All status values are defined as individual constants plus grouped lists:

```python
# Individual constants
TASK_STATUS_PENDING: str = "pending"
TASK_STATUS_IN_PROGRESS: str = "in_progress"
TASK_STATUS_COMPLETED: str = "completed"
TASK_STATUS_ARCHIVED: str = "archived"

# Grouped list for validation
TASK_STATUSES: list[str] = [
    TASK_STATUS_PENDING,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_ARCHIVED,
]
```

**Usage:**
```python
from app.constants import TASK_STATUS_PENDING, TASK_STATUSES

# Create task with default status
task = Task(title="My Task", status=TASK_STATUS_PENDING)

# Validate status
if task.status in TASK_STATUSES:
    print("Valid status!")
```

### Priority Constants

```python
TASK_PRIORITY_LOW: str = "low"
TASK_PRIORITY_MEDIUM: str = "medium"
TASK_PRIORITY_HIGH: str = "high"
TASK_PRIORITY_CRITICAL: str = "critical"

TASK_PRIORITIES: list[str] = [...]
DEFAULT_TASK_PRIORITY: str = TASK_PRIORITY_MEDIUM
```

**Usage:**
```python
from app.constants import TASK_PRIORITIES, DEFAULT_TASK_PRIORITY

# Validate priority
if priority not in TASK_PRIORITIES:
    raise ValidationError(f"Invalid priority. Must be: {TASK_PRIORITIES}")

# Use default
task.priority = DEFAULT_TASK_PRIORITY
```

### Validation Constraints

```python
# Length constraints
TASK_TITLE_MIN_LENGTH: int = 3
TASK_TITLE_MAX_LENGTH: int = 200

CATEGORY_NAME_MIN_LENGTH: int = 2
CATEGORY_NAME_MAX_LENGTH: int = 50
```

**Usage:**
```python
from app.constants import TASK_TITLE_MIN_LENGTH, TASK_TITLE_MAX_LENGTH

class TaskValidator(BaseValidator):
    def validate(self, title: str) -> Tuple[bool, Optional[str]]:
        if len(title) < TASK_TITLE_MIN_LENGTH:
            return False, f"Title must be at least {TASK_TITLE_MIN_LENGTH} chars"
        if len(title) > TASK_TITLE_MAX_LENGTH:
            return False, f"Title must be at most {TASK_TITLE_MAX_LENGTH} chars"
        return True, None
```

### Color Constants

```python
COLOR_RED: str = "#FF5733"
COLOR_BLUE: str = "#0066FF"
COLOR_GREEN: str = "#00CC66"

DEFAULT_CATEGORY_COLORS: list[str] = [
    COLOR_RED,
    COLOR_BLUE,
    COLOR_GREEN,
    # ...
]
```

**Usage:**
```python
from app.constants import DEFAULT_CATEGORY_COLORS

# Validate category color
if color not in DEFAULT_CATEGORY_COLORS:
    raise ValidationError(f"Invalid color. Choose from: {DEFAULT_CATEGORY_COLORS}")
```

### Pagination & Limits

```python
DEFAULT_PAGE_SIZE: int = 10
MAX_PAGE_SIZE: int = 100
MIN_PAGE_SIZE: int = 1

DEFAULT_LIMIT: int = 50
MAX_LIMIT: int = 1000
```

### Time Constants

```python
TASK_DUE_SOON_DAYS: int = 3  # Consider task due if within 3 days
NOTIFICATION_RETENTION_DAYS: int = 30  # Keep notifications for 30 days
ARCHIVED_ITEM_RETENTION_DAYS: int = 90  # Keep archived items for 90 days
```

**Usage:**
```python
from app.constants import TASK_DUE_SOON_DAYS
from datetime import datetime, timedelta

def is_task_due_soon(due_date):
    today = datetime.now().date()
    threshold = today + timedelta(days=TASK_DUE_SOON_DAYS)
    return due_date <= threshold
```

### Error Messages

```python
# Validation errors
ERROR_INVALID_EMAIL: str = "Invalid email format"
ERROR_INVALID_NAME: str = "Name is required and must be 2-100 characters"

# Not found errors
ERROR_TASK_NOT_FOUND: str = "Task not found"
ERROR_PROJECT_NOT_FOUND: str = "Project not found"

# Conflict errors
ERROR_DUPLICATE_TAG: str = "Tag with this name already exists"
```

**Usage:**
```python
from app.constants import ERROR_TASK_NOT_FOUND

def get_task(task_id):
    task = repo.get(task_id)
    if not task:
        raise NotFoundError(ERROR_TASK_NOT_FOUND)
    return task
```

### Success Messages

```python
SUCCESS_TASK_CREATED: str = "Task created successfully"
SUCCESS_TASK_UPDATED: str = "Task updated successfully"
SUCCESS_TASK_DELETED: str = "Task deleted successfully"
```

**Usage:**
```python
from app.constants import SUCCESS_TASK_CREATED
from app.common import SuccessResponse

response = SuccessResponse(
    message=SUCCESS_TASK_CREATED,
    data=task.to_dict(),
    status_code=HTTP_CREATED
)
```

### API Response Codes

```python
HTTP_OK: int = 200
HTTP_CREATED: int = 201
HTTP_BAD_REQUEST: int = 400
HTTP_NOT_FOUND: int = 404
HTTP_CONFLICT: int = 409
HTTP_INTERNAL_ERROR: int = 500
```

### Type Aliases

```python
TaskID: TypeAlias = int
ProjectID: TypeAlias = int
UserID: TypeAlias = int
```

**Usage:**
```python
from app.constants import TaskID

def get_task(task_id: TaskID) -> Task:
    return repo.get(task_id)

def complete_task(task_id: TaskID) -> bool:
    task = repo.get(task_id)
    task.status = TASK_STATUS_COMPLETED
    return True
```

### Application Config

```python
APP_NAME: str = "TODO Management System"
APP_VERSION: str = "1.0.0"
APP_DESCRIPTION: str = "..."

DEBUG_MODE: bool = False
VERBOSE_LOGGING: bool = False
```

### DateTime Formats

```python
ISO_DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
ISO_DATE_FORMAT: str = "%Y-%m-%d"
READABLE_DATETIME_FORMAT: str = "%B %d, %Y %H:%M:%S"
```

**Usage:**
```python
from app.constants import ISO_DATETIME_FORMAT
from datetime import datetime

def format_timestamp(dt: datetime) -> str:
    return dt.strftime(ISO_DATETIME_FORMAT)
```

---

## ✅ How Code Rabbit Should Detect Issues

### ❌ Bad: Using magic strings/numbers

```python
# ❌ Bad: Magic number
def validate_title(title):
    if len(title) < 3:  # What does 3 mean?
        return False
    return True

# ✅ Good: Using constant
from app.constants import TASK_TITLE_MIN_LENGTH

def validate_title(title):
    if len(title) < TASK_TITLE_MIN_LENGTH:
        return False
    return True
```

### ❌ Bad: Inconsistent values

```python
# ❌ Bad: Different status values in different places
def create_task():
    return Task(status="pending")  # Different from constant!

def get_pending_tasks():
    return [t for t in tasks if t.status == "PENDING"]  # Different case!

# ✅ Good: Use constants consistently
from app.constants import TASK_STATUS_PENDING

def create_task():
    return Task(status=TASK_STATUS_PENDING)

def get_pending_tasks():
    return [t for t in tasks if t.status == TASK_STATUS_PENDING]
```

### ❌ Bad: Hardcoded error messages

```python
# ❌ Bad: Hardcoded message
if not task:
    raise NotFoundError("Task not found")  # What if message changes?

# ✅ Good: Use constant
from app.constants import ERROR_TASK_NOT_FOUND

if not task:
    raise NotFoundError(ERROR_TASK_NOT_FOUND)
```

---

## 📊 Import Patterns

### Pattern 1: Import Specific Constants
```python
from app.constants import TASK_STATUS_PENDING, TASK_STATUSES, TASK_TITLE_MIN_LENGTH

status = TASK_STATUS_PENDING
max_title = TASK_TITLE_MAX_LENGTH
```

### Pattern 2: Import All Constants
```python
import app.constants as const

status = const.TASK_STATUS_PENDING
max_title = const.TASK_TITLE_MAX_LENGTH
```

### Pattern 3: From App Package
```python
from app import TASK_STATUS_PENDING, SUCCESS_TASK_CREATED

task = Task(status=TASK_STATUS_PENDING)
response = SuccessResponse(message=SUCCESS_TASK_CREATED)
```

---

## 🎓 Best Practices

1. **Always use constants for repeated values**
   ```python
   # ❌ Bad
   if status == "pending": ...
   if status == "pending": ...  # Repeated!
   
   # ✅ Good
   from app.constants import TASK_STATUS_PENDING
   if status == TASK_STATUS_PENDING: ...
   if status == TASK_STATUS_PENDING: ...  # DRY principle
   ```

2. **Use grouped lists for validation**
   ```python
   # ✅ Good
   if status not in TASK_STATUSES:
       raise ValidationError(f"Invalid status")
   ```

3. **Prefer UPPER_CASE for module-level constants**
   ```python
   # ✅ Good - follows Python convention
   MAX_RETRIES: int = 3
   DEFAULT_TIMEOUT: int = 30
   
   # ❌ Bad - wrong naming
   max_retries: int = 3
   defaultTimeout: int = 30
   ```

4. **Use type hints**
   ```python
   # ✅ Good - type-safe
   DEFAULT_PAGE_SIZE: int = 10
   APP_NAME: str = "TODO App"
   
   # ❌ Bad - no type info
   DEFAULT_PAGE_SIZE = 10
   APP_NAME = "TODO App"
   ```

5. **Group related constants**
   ```python
   # ✅ Good - organized by category
   # Task Statuses
   TASK_STATUS_PENDING: str = "pending"
   TASK_STATUS_COMPLETED: str = "completed"
   
   # Project Statuses
   PROJECT_STATUS_ACTIVE: str = "active"
   PROJECT_STATUS_ARCHIVED: str = "archived"
   ```

---

## 🧪 Testing Constants

When testing, you can safely use constants:

```python
import unittest
from app.constants import TASK_STATUS_PENDING, TASK_TITLE_MIN_LENGTH

class TestTask(unittest.TestCase):
    def test_task_default_status(self):
        task = Task(title="Test")
        self.assertEqual(task.status, TASK_STATUS_PENDING)
    
    def test_task_title_validation(self):
        title = "a" * (TASK_TITLE_MIN_LENGTH - 1)
        is_valid, _ = validate_title(title)
        self.assertFalse(is_valid)
```

---

Perfect for testing constant usage in Code Rabbit reviews! 🚀
