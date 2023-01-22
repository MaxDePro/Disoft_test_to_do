from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, CommentForm
from .models import Task, Comment
from django.db.models import Q


def change_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status != 'In Progress':
        task.status = 'In Progress'
    task.save()
    return redirect('task_detail', task_id=task_id)


@login_required
def task_list(request):
    # Check if user is admin, allow view all tasks
    if request.user.is_superuser:
        # Getting all tasks
        tasks = Task.objects.all()
        # Filtering for status
        status = request.GET.get('status')
        if status:
            tasks = tasks.filter(status=status)
        return render(request, 'to_do_taskmanager/task_list.html', {'tasks': tasks})
    # Check if user is author of task, allow user to see his tasks
    elif Task.objects.filter(author=request.user) or Task.objects.filter(assigned_to=request.user):
        # Getting tasks where user is author or assigned to user
        tasks = Task.objects.filter(Q(author=request.user) | Q(assigned_to=request.user)).distinct()
        # Filter tasks with status
        status = request.GET.get('status')
        if status:
            tasks = tasks.filter(status=status)
        return render(request, 'to_do_taskmanager/task_list.html', {'tasks': tasks})
    return render(request, 'to_do_taskmanager/task_list.html', {})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    can_change_status = False
    if task.assigned_to.all():
        for assigned_user in task.assigned_to.all():
            if assigned_user == user:
                can_change_status = True
                break
    comments = Comment.objects.filter(task=task)
    user = request.user
    can_comment = False
    if user.is_authenticated:
        if user == task.author or user.is_staff or task.assigned_to.filter(id=user.id).exists():
            can_comment = True
    context = {'task': task, 'comments': comments, 'can_comment': can_comment, 'can_change_status': can_change_status}
    return render(request, 'to_do_taskmanager/task_detail.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            # task = form.save(commit=False)
            # task.author = request.user
            # task.save()
            return redirect('task_detail', task_id=task.pk)
    else:
        form = TaskForm()
    context = {'form': form}
    return render(request, 'to_do_taskmanager/task_form.html', context)


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not request.user.is_authenticated:
        messages.success(request, 'You have no permissions for this')
        return redirect('task_list')
    if not request.user.is_superuser and request.user != task.author:
        messages.success(request, 'You have no permissions for this')
        return redirect('task_list')
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.pk)
    else:
        form = TaskForm(instance=task)
    context = {'form': form}
    return render(request, 'to_do_taskmanager/task_form.html', context)


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not request.user.is_authenticated:
        messages.success(request, 'You have no permissions for this')
        return redirect('task_list')
    if not request.user.is_superuser and request.user != task.author:
        messages.success(request, 'You have no permissions for this')
        return redirect('task_list')
    task.delete()
    messages.success(request, 'Task successful deleted')
    return redirect('task_list')


@login_required
def comment_create(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = task
            comment.save()
            return redirect('task_detail', task_id=task.pk)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'to_do_taskmanager/comment_form.html', context)


def home_page(request):
    return render(request, 'to_do_taskmanager/home.html')


# Create a function to logout user
def logout_user(request):
    # Use django logout method
    logout(request)
    # messages.success(request, 'You were logout!')
    return redirect('home_page')


# Create a function to login user into system
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Use django authenticate method
        user = authenticate(request, username=username, password=password)
        # If data set correct we login into system
        if user is not None:
            login(request, user)
            return redirect('home_page')
        # If data is incorrect we have an error
        else:
            messages.success(request, 'Yo have failed to login, Try again')
            return redirect('login_user')
    else:
        return render(request, 'to_do_taskmanager/login_user.html', {})
