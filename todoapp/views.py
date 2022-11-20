from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Todo


@login_required
def todo_set_done(request, todo_id):
    is_done = request.GET.get("done", True)

    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE todoapp_todo SET done = %s WHERE id = %s", [is_done, str(todo_id)]
        )

    return redirect("/" if not is_done else "/todos/completed/")


@login_required
def todo_add_view(request):
    if request.method == "POST":
        todo = Todo(user=request.user, text=request.POST.get("text"))
        todo.save()
    return redirect("/")


@login_required
def todo_list_view(request, list_completed_todos=False):
    todos = Todo.objects.filter(user=request.user, done=list_completed_todos)

    return render(
        request,
        "todos.html",
        {"todos": todos, "list_completed_todos": list_completed_todos},
    )
