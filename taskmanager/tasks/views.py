from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm, UserRegistrationForm
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'tasks/register.html', {'form': form})

@login_required
def task_list(request):
    created_tasks = Task.objects.filter(created_by=request.user).order_by('due_date')
    assigned_tasks = Task.objects.filter(assigned_to=request.user).exclude(created_by=request.user).order_by('due_date')
    employees = User.objects.filter(is_active=True).order_by('username')
    
    return render(request, 'tasks/task_list.html', {
        'created_tasks': created_tasks,
        'assigned_tasks': assigned_tasks,
        'employees': employees
    })

@login_required
def task_assign(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, created_by=request.user)
        assigned_to_id = request.POST.get('assigned_to')
        
        if assigned_to_id:
            employee = get_object_or_404(User, id=assigned_to_id)
            task.assigned_to.clear()
            task.assigned_to.add(employee)
            messages.success(request, f'Task assigned to {employee.get_full_name() or employee.username}')
        else:
            task.assigned_to.clear()
            messages.success(request, 'Task assignment removed')
            
    return redirect('task_list')
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.assigned_to.add(request.user)
        messages.success(request, 'Task assigned to you successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update'})
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task successfully deleted.')
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})