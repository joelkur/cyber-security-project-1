from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Todo


@login_required
def todo_delete(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)

    # if todo.user != request.user:
    #    return HttpResponseForbidden()

    todo.delete()
    return redirect("/")


@login_required
def todo_set_done(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)

    # if todo.user != request.user:
    #    return HttpResponseForbidden()

    todo.done = not todo.done
    todo.save()
    return redirect("/" if todo.done else "/todos/completed/")


@login_required
@csrf_exempt
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

    # Better way to get list of todos without SQL injection
    # todos = Todo.objects.filter(
    #     user=request.user,
    #     done=list_completed_todos,
    #     text__contains=search,
    # )

    # Another fix via prepared statement
    # query = f"SELECT id, text, done FROM todoapp_todo WHERE user_id = %s AND done = %s AND text LIKE %s"
    # todos = Todo.objects.raw(
    #     query, [request.user.id, list_completed_todos, f"%{search}%"]
    # )

    return render(
        request,
        "todos.html",
        {"todos": todos, "list_completed_todos": list_completed_todos},
    )
