"""
Main TODO application demo.
Demonstrates all components working together following established patterns.
"""

import logging
from app.models.task import TaskStatus, TaskPriority
from app.models.project import ProjectStatus
from app.models.notification import NotificationStatus, NotificationType
from app.services.task_service import TaskRepository
from app.services.project_service import ProjectRepository
from app.services.category_service import CategoryRepository
from app.services.tag_service import TagRepository
from app.services.notification_service import NotificationRepository
from app.common.exceptions import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def demo_project_management():
    """Demonstrate project management using common patterns."""
    logger.info("\n" + "="*60)
    logger.info("PROJECT MANAGEMENT DEMO")
    logger.info("="*60)

    # Initialize repository (following BaseRepository pattern)
    project_repo = ProjectRepository()

    # Create projects
    project1 = project_repo.create(
        name="Website Redesign",
        description="Complete redesign of company website",
        owner_id=1,
        status=ProjectStatus.PLANNING,
    )
    logger.info(f"Created project: {project1}")

    project2 = project_repo.create(
        name="Mobile App",
        description="New mobile app development",
        owner_id=1,
        status=ProjectStatus.ACTIVE,
    )
    logger.info(f"Created project: {project2}")

    # Activate project
    project1.activate()
    logger.info(f"Activated project: {project1.name}")

    # Add members
    project1.add_member(2)
    project1.add_member(3)
    logger.info(f"Project members: {project1.members}")

    # Find active projects
    active_projects = project_repo.find_active()
    logger.info(f"Active projects: {[p.name for p in active_projects]}")

    # Get user's projects
    user_projects = project_repo.get_user_projects(1)
    logger.info(f"User 1 projects: {[p.name for p in user_projects]}")


def demo_task_management():
    """Demonstrate task management using common patterns."""
    logger.info("\n" + "="*60)
    logger.info("TASK MANAGEMENT DEMO")
    logger.info("="*60)

    # Initialize repository (following BaseRepository pattern)
    task_repo = TaskRepository()
    project_repo = ProjectRepository()

    # Create a project first
    project = project_repo.create("Learn Python", owner_id=1)

    # Create tasks
    task1 = task_repo.create(
        title="Learn decorators",
        description="Study advanced decorators",
        project_id=project.id,
        priority=TaskPriority.HIGH,
    )
    logger.info(f"Created task: {task1}")

    task2 = task_repo.create(
        title="Build TODO app",
        description="Create a complete TODO application",
        project_id=project.id,
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.CRITICAL,
    )
    logger.info(f"Created task: {task2}")

    task3 = task_repo.create(
        title="Write tests",
        description="Add unit tests",
        project_id=project.id,
        priority=TaskPriority.HIGH,
    )
    logger.info(f"Created task: {task3}")

    # Add tags
    task1.add_tag("learning")
    task2.add_tag("development")
    logger.info(f"Task 1 tags: {task1.tags}")

    # Mark task as done
    task3.mark_as_done()
    logger.info(f"Completed task: {task3.title}")

    # Find tasks by status
    in_progress = task_repo.find_by_status(TaskStatus.IN_PROGRESS)
    logger.info(f"In progress tasks: {[t.title for t in in_progress]}")

    # Find tasks by priority
    high_priority = task_repo.find_by_priority(TaskPriority.HIGH)
    logger.info(f"High priority tasks: {[t.title for t in high_priority]}")

    # Find tasks by tag
    learning_tasks = task_repo.find_by_tag("learning")
    logger.info(f"Learning tasks: {[t.title for t in learning_tasks]}")

    # Show task count
    logger.info(f"Total tasks: {task_repo.count()}")


def demo_tag_management():
    """Demonstrate tag management using common patterns."""
    logger.info("\n" + "="*60)
    logger.info("TAG MANAGEMENT DEMO")
    logger.info("="*60)

    # Initialize repository (following BaseRepository pattern)
    tag_repo = TagRepository()

    # Create tags
    tag1 = tag_repo.create("urgent")
    tag2 = tag_repo.create("documentation")
    tag3 = tag_repo.create("bug")

    logger.info(f"Created tags: {tag1.name}, {tag2.name}, {tag3.name}")

    # Increment usage
    tag1.increment_usage()
    tag1.increment_usage()
    tag2.increment_usage()
    logger.info(f"Tag usage counts: urgent={tag1.usage_count}, doc={tag2.usage_count}")

    # Get popular tags
    popular = tag_repo.get_popular_tags(2)
    logger.info(f"Popular tags: {[t.name for t in popular]}")


def demo_category_management():
    """Demonstrate category management using common patterns."""
    logger.info("\n" + "="*60)
    logger.info("CATEGORY MANAGEMENT DEMO")
    logger.info("="*60)

    # Initialize repository (following BaseRepository pattern)
    category_repo = CategoryRepository()

    # Create categories
    work = category_repo.create(
        name="Work",
        color="#FF5733",
        description="Work-related tasks",
    )
    personal = category_repo.create(
        name="Personal",
        color="#33FF57",
        description="Personal tasks",
    )
    logger.info(f"Created categories: {work.name}, {personal.name}")

    # Find categories by name
    found = category_repo.find_by_name("work")
    logger.info(f"Found categories: {[c.name for c in found]}")

    # Get by exact name
    work_cat = category_repo.get_by_name("Work")
    logger.info(f"Work category color: {work_cat.color}")


def demo_notification_management():
    """Demonstrate notification management using established patterns."""
    logger.info("\n" + "="*60)
    logger.info("NOTIFICATION MANAGEMENT DEMO")
    logger.info("="*60)
    logger.info("\nDemonstrates Notification model and NotificationRepository")
    logger.info("following the same patterns as Task, Project, Category, Tag.\n")

    # Initialize repository (following BaseRepository pattern)
    notification_repo = NotificationRepository()

    # Create notifications for user 1
    notif1 = notification_repo.create(
        user_id=1,
        message="Task 'Buy groceries' has been assigned to you",
        notification_type=NotificationType.TASK_ASSIGNED,
        related_entity_id=1,
        related_entity_type="Task",
    )
    logger.info(f"Created notification: {notif1.message}")

    notif2 = notification_repo.create(
        user_id=1,
        message="Task 'Complete project' is due soon",
        notification_type=NotificationType.TASK_DUE_SOON,
        related_entity_id=2,
        related_entity_type="Task",
    )
    logger.info(f"Created notification: {notif2.message}")

    notif3 = notification_repo.create(
        user_id=1,
        message="Project 'Website Redesign' has been updated",
        notification_type=NotificationType.PROJECT_UPDATED,
        related_entity_id=1,
        related_entity_type="Project",
    )
    logger.info(f"Created notification: {notif3.message}")

    # Find all unread notifications for user 1
    logger.info("\nFinding unread notifications for user 1...")
    unread = notification_repo.find_unread(user_id=1)
    logger.info(f"Found {len(unread)} unread notifications")
    for notif in unread:
        logger.info(f"  - [{notif.notification_type.value}] {notif.message}")

    # Get unread count
    unread_count = notification_repo.get_unread_count(user_id=1)
    logger.info(f"Unread count for user 1: {unread_count}")

    # Find notifications by type
    logger.info("\nFinding TASK_ASSIGNED notifications...")
    assigned_notifs = notification_repo.find_by_type(NotificationType.TASK_ASSIGNED)
    logger.info(f"Found {len(assigned_notifs)} TASK_ASSIGNED notifications")

    # Mark first notification as read
    logger.info(f"\nMarking notification {notif1.id} as read...")
    notification_repo.mark_as_read(notif1.id)
    logger.info(f"Notification status: {notif1.status.value}")

    # Check unread count after marking as read
    updated_unread = notification_repo.get_unread_count(user_id=1)
    logger.info(f"Updated unread count for user 1: {updated_unread}")

    # Archive a notification
    logger.info(f"\nArchiving notification {notif2.id}...")
    notification_repo.archive(notif2.id)
    logger.info(f"Notification archived, status: {notif2.status.value}")

    # Demonstrate serialization (pattern used across all models)
    logger.info("\nNotification serialization (to_dict):")
    logger.info(f"{notif3.to_dict()}")


def demo_error_handling():
    """Demonstrate error handling with custom exceptions."""
    logger.info("\n" + "="*60)
    logger.info("ERROR HANDLING DEMO")
    logger.info("="*60)

    task_repo = TaskRepository()

    # Test validation error
    try:
        invalid_task = task_repo.create("", "No title")
    except ValidationError as e:
        logger.error(f"Validation error: {e.message}")

    # Test duplicate tag
    tag_repo = TagRepository()
    tag_repo.create("important")
    try:
        tag_repo.create("important")
    except ValidationError as e:
        logger.error(f"Duplicate error: {e.message}")

    # Test not found
    try:
        task_repo.get_or_raise(999, "Task")
    except Exception as e:
        logger.error(f"Not found: {e}")


def main() -> None:
    """Main entry point."""
    logger.info("\n" + "="*60)
    logger.info("TODO APPLICATION - SHARED COMPONENTS DEMO")
    logger.info("="*60)
    logger.info("\nThis demo shows how shared components are used across")
    logger.info("multiple entities following common patterns.\n")

    demo_project_management()
    demo_task_management()
    demo_category_management()
    demo_tag_management()
    demo_notification_management()
    demo_error_handling()

    logger.info("\n" + "="*60)
    logger.info("DEMO COMPLETE")
    logger.info("="*60)
    logger.info("\nKey components demonstrated:")
    logger.info("✓ BaseModel - Used by Task, Project, Category, Tag, Notification")
    logger.info("✓ BaseRepository - Used by all services")
    logger.info("✓ Custom exceptions - ValidationError, NotFoundError, etc")
    logger.info("✓ Validation pattern - Applied consistently")
    logger.info("✓ Service layer - Separates logic from models")
    logger.info("✓ Pattern reuse - Notification follows established patterns")
    logger.info("\nNow create a PR that violates these patterns!")
    logger.info("Code Rabbit should detect the violations.\n")


if __name__ == "__main__":
    main()
