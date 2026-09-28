from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Building


def home(request):
    return render(request, "build/index.html")


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "build/login.html")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "build/login.html")


@login_required
def dashboard(request):

    buildings = Building.objects.all().order_by("-created_at")

    total = buildings.count()
    active = buildings.filter(status="Active").count()
    inactive = buildings.filter(status="Inactive").count()
    maintenance = buildings.filter(status="Maintenance").count()

    context = {
        "buildings": buildings,
        "total": total,
        "active": active,
        "inactive": inactive,
        "maintenance": maintenance,
    }

    return render(
        request,
        "build/dashboard.html",
        context,
    )


@login_required
def add_building(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "Active")

        if not name:
            messages.error(
                request,
                "Building name is required."
            )

            return render(
                request,
                "build/add_data.html",
            )

        Building.objects.create(
            name=name,
            location=location,
            description=description,
            status=status,
        )

        messages.success(
            request,
            "Building added successfully."
        )

        return redirect("dashboard")

    return render(
        request,
        "build/add_data.html",
    )


@login_required
def building_detail(request, id):

    building = get_object_or_404(
        Building,
        id=id,
    )

    return render(
        request,
        "build/building_detail.html",
        {
            "building": building,
        },
    )


@login_required
def edit_building(request, id):

    building = get_object_or_404(
        Building,
        id=id,
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()

        if not name:

            messages.error(
                request,
                "Building name is required."
            )

            return render(
                request,
                "build/edit_building.html",
                {
                    "building": building,
                },
            )

        building.name = name
        building.location = request.POST.get(
            "location",
            ""
        ).strip()

        building.description = request.POST.get(
            "description",
            ""
        ).strip()

        building.status = request.POST.get(
            "status",
            "Active"
        )

        building.save()

        messages.success(
            request,
            "Building updated successfully."
        )

        return redirect(
            "building_detail",
            id=building.id,
        )

    return render(
        request,
        "build/edit_building.html",
        {
            "building": building,
        },
    )


@login_required
def delete_building(request, id):

    building = get_object_or_404(
        Building,
        id=id,
    )

    if request.method == "POST":

        building_name = building.name

        building.delete()

        messages.success(
            request,
            f'"{building_name}" was deleted successfully.'
        )

        return redirect("dashboard")

    return render(
        request,
        "build/delete_building.html",
        {
            "building": building,
        },
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")
