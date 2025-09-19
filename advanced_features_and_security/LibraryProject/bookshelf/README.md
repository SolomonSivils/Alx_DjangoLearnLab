# Django Permissions Setup

This application uses a custom permissions and groups system to control user access to `Article` model operations.

## Custom Permissions
The `blog.models.Article` model defines four custom permissions within its `Meta` class:
- `can_view`: Allows a user to view a list of articles.
- `can_create`: Allows a user to create new articles.
- `can_edit`: Allows a user to edit existing articles.
- `can_delete`: Allows a user to delete articles.

## User Groups
The following groups are configured in the Django admin to manage these permissions:
- **Admins**: Have all four permissions (`can_view`, `can_create`, `can_edit`, `can_delete`).
- **Editors**: Have `can_view`, `can_create`, and `can_edit`.
- **Viewers**: Have only `can_view`.

## Enforcing Permissions in Views
The `@permission_required` decorator from `django.contrib.auth.decorators` is used on views to check for the required permission before executing the view logic. For example, the `article_edit` view is protected by `@permission_required('blog.can_edit')`.