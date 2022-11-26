from django.urls import path

from .views import todo_list_view, todo_add_view, todo_set_done, todo_delete

urlpatterns = [
    path("todos/<int:todo_id>/delete/", todo_delete, name="todo_delete"),
    path(
        "todos/completed/",
        todo_list_view,
        {"list_completed_todos": True},
        name="completed_todos",
    ),
    path("todos/<int:todo_id>/set-done/", todo_set_done, name="todo_set_done"),
    path("todos", todo_add_view, name="add_todo"),
    path("", todo_list_view, name="todos"),
]
