from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Todo


@login_required
def todo_delete(request, todo_id):
    Todo.objects.filter(pk=todo_id).delete()
    return redirect("/")


@login_required
def todo_set_done(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.done = not todo.done
    todo.save()
    return redirect("/" if todo.done else "/todos/completed/")


@login_required
def todo_add_view(request):
    if request.method == "POST":
        todo = Todo(user=request.user, text=request.POST.get("text"))
        todo.save()
    return redirect("/")


@login_required
def todo_list_view(request, list_completed_todos=False):
    search = request.GET.get("search", "")
    query = f"SELECT id, text, done FROM todoapp_todo WHERE user_id = {request.user.id} AND done = {list_completed_todos} AND text LIKE '%{search}%'"
    todos = Todo.objects.raw(query)
    return render(
        request,
        "todos.html",
        {"todos": todos, "list_completed_todos": list_completed_todos},
    )
