# TODO Management Application

A comprehensive TODO/Task Management application designed to demonstrate **shared components and reusable patterns** across multiple entities. Perfect for testing code review automation tools.

## 🎯 Purpose

This project establishes clear, consistent patterns across the entire codebase:
- **BaseModel** - All entities inherit from this
- **BaseRepository** - All services follow this pattern
- **Custom Exceptions** - Consistent error handling
- **Validation** - Applied uniformly
- **Response Models** - Standardized API responses

You can create feature branches that **violate these patterns** to test if Code Rabbit can detect them.

## 📦 Project Structure

```
todo-project/
├── app/
│   ├── common/                    # SHARED COMPONENTS (key!)
│   │   ├── __init__.py
│   │   ├── base.py               # BaseModel, BaseRepository
│   │   ├── exceptions.py          # AppException, ValidationError, NotFoundError
│   │   ├── response.py            # ResponseModel, SuccessResponse, ErrorResponse
│   │   └── validators.py          # BaseValidator, specific validators
│   │
│   ├── models/                    # Entities using BaseModel
│   │   ├── task.py               # Task (uses BaseModel)
│   │   ├── project.py            # Project (uses BaseModel)
│   │   ├── category.py           # Category (uses BaseModel)
│   │   └── tag.py                # Tag (uses BaseModel)
│   │
│   ├── services/                 # Repositories using BaseRepository
│   │   ├── task_service.py       # TaskRepository (uses BaseRepository)
│   │   ├── project_service.py    # ProjectRepository (uses BaseRepository)
│   │   ├── category_service.py   # CategoryRepository (uses BaseRepository)
│   │   └── tag_service.py        # TagRepository (uses BaseRepository)
│   │
│   └── utils/                     # Utilities
│
├── tests/
│   ├── test_task.py
│   └── test_project.py
│
├── main.py                        # Demo showing patterns in action
└── requirements.txt
```

## 🏗️ Established Patterns

### 1. **BaseModel Pattern** (Used by: Task, Project, Category, Tag)

All entities inherit from `BaseModel` and implement:
- `validate()` - Returns Tuple[bool, Optional[str]]
- `to_dict()` - Serialization
- Common attributes: `id`, `created_at`, `updated_at`

```python
class Task(BaseModel):
    def validate(self) -> Tuple[bool, Optional[str]]:
        if not self.title:
            return False, "Title is required"
        return True, None
    
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "title": self.title, ...}
```

### 2. **BaseRepository Pattern** (Used by: TaskRepository, ProjectRepository, CategoryRepository, TagRepository)

All repositories inherit from `BaseRepository[T]` and implement:
- `create(**kwargs) -> T` - Create with validation
- Inherited: `get()`, `get_all()`, `update()`, `delete()`, `count()`, `exists()`
- Custom finders: `find_by_status()`, `find_by_tag()`, etc.

```python
class TaskRepository(BaseRepository[Task]):
    def create(self, title: str, ...) -> Task:
        task = Task(...)
        is_valid, error = task.validate()
        if not is_valid:
            raise ValidationError(error)
        self._items[task.id] = task
        return task
```

### 3. **Exception Handling Pattern**

Uses custom exceptions hierarchy:
- `AppException` - Base exception
- `ValidationError` - When validation fails
- `NotFoundError` - When resource not found
- `ConflictError` - When resource conflicts (duplicates)

### 4. **Validation Pattern**

All entities validate before storage:
```python
task = Task(...)
is_valid, error = task.validate()
if not is_valid:
    raise ValidationError(error)
```

## 🚀 Quick Start

### Installation

```bash
# Clone and setup
git clone <repo>
cd todo-project

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Demo

```bash
python main.py
```

Shows all components working together following established patterns.

### Run Tests

```bash
python -m unittest discover tests -v
```

## 📋 Entity Examples

### Task (Product Entity)
- Uses `BaseModel` for structure
- Implements validation
- Has status (TODO, IN_PROGRESS, DONE, BLOCKED)
- Has priority (LOW, MEDIUM, HIGH, CRITICAL)
- Can be overdue, marked done, tagged

### Project (Container Entity)
- Uses `BaseModel` for structure
- Has members and progress tracking
- Can be activated/archived
- Groups tasks together

### Category & Tag (Reference Entities)
- Use `BaseModel` for consistency
- Validate color format
- Track usage counts

## 🔄 Using Shared Components

### Creating a Task
```python
from app.services.task_service import TaskRepository
from app.models.task import TaskStatus, TaskPriority
from app.common.exceptions import ValidationError

repo = TaskRepository()

try:
    task = repo.create(
        title="New Task",
        priority=TaskPriority.HIGH,
        status=TaskStatus.TODO,
    )
except ValidationError as e:
    print(f"Validation failed: {e.message}")
```

### Creating a Project
```python
from app.services.project_service import ProjectRepository
from app.models.project import ProjectStatus

repo = ProjectRepository()

try:
    project = repo.create(
        name="New Project",
        owner_id=1,
        status=ProjectStatus.PLANNING,
    )
except ValidationError as e:
    print(f"Validation failed: {e.message}")
```

## 🧪 Testing Patterns

All tests demonstrate:
- Model validation
- Repository CRUD operations
- Custom exception handling
- Finder methods

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test
python -m unittest tests.test_task.TestTaskModel
```

## 🎯 What to Test with Code Rabbit

Create PRs that violate these patterns:

### ❌ Bad Patterns (To Test Detection):
1. **Skip BaseModel** - Create a model without inheriting BaseModel
2. **Skip BaseRepository** - Implement repository without BaseRepository
3. **Skip validation** - Create entities without validation
4. **Wrong exception types** - Use ValueError instead of ValidationError
5. **Inconsistent to_dict()** - Different serialization approach
6. **Missing error handling** - Don't catch exceptions properly
7. **Inline logic** - Put repository logic in models
8. **No docstrings** - Skip documentation

### ✅ Good Patterns (Already Established):
1. All models extend BaseModel
2. All repositories extend BaseRepository[T]
3. Validation before storage
4. Custom exceptions for errors
5. Consistent serialization
6. Proper error handling
7. Separation of concerns
8. Comprehensive documentation

## 📊 Metrics for Code Rabbit Testing

This project is designed to test:
- **Pattern Detection** - Does it identify BaseModel/BaseRepository usage?
- **Inheritance Tracking** - Does it understand class hierarchies?
- **Error Handling** - Can it flag missing exception handling?
- **Validation Logic** - Does it recognize validation patterns?
- **Code Consistency** - Can it detect deviations from established patterns?
- **Code Graph Accuracy** - Does code graph show correct dependencies?
- **Embeddings** - Do embeddings capture semantic meaning?

## 🔗 Component Dependencies

```
common/ (Shared)
├── exceptions.py → Used by all services
├── validators.py → Used in models for validation
├── response.py → For API responses
└── base.py → BaseModel (inherited by all models)
              BaseRepository (inherited by all services)

models/ (All use BaseModel)
├── task.py
├── project.py
├── category.py
└── tag.py

services/ (All use BaseRepository)
├── task_service.py
├── project_service.py
├── category_service.py
└── tag_service.py
```

## 📝 Next Steps

1. **Clone this repo** ✓
2. **Run `python main.py`** to see patterns in action
3. **Run tests** with `python -m unittest discover tests`
4. **Create a feature branch** and add a feature that:
   - Violates one or more patterns
   - Is functional but "wrong"
5. **Create a PR** for that feature
6. **Share with Code Rabbit** for code review
7. **Verify** if Code Rabbit detects the pattern violations

## 🎓 Learning

This project teaches:
- How to establish patterns across a codebase
- Inheritance and polymorphism
- Repository pattern
- Exception handling
- Validation patterns
- Consistent API design

## 📄 License

MIT License

---

**Perfect for testing Code Review Automation!** 🚀

The clear pattern established makes it easy to create "bad" code that violates norms, and see if Code Rabbit can detect these violations accurately.
