from django.apps.registry import apps
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

workspaces = [
    {"id": 1, "name": "Workspace1", "is_active": False},
    {"id": 2, "name": "Workspace2", "is_active": False},
]

visualizers = [
    {
        "id": 1,
        "name": "Simple visualizer",
    },
    {"id": 2, "name": "Block visualizer"},
]


# Create your views here.
def index(request):
    return render(
        request,
        "index.html",
        {"workspaces": workspaces, "visualizers": visualizers},
    )


def workspace(request, workspace_id):
    for w in workspaces:
        if w["id"] == int(workspace_id):
            w["is_active"] = True
        else:
            w["is_active"] = False
    return render(
        request,
        "index.html",
        {
            "workspaces": workspaces,
            "visualizers": visualizers,
            #"selected_visualizer_id": 1,
        },
    )


def select_visualizer(_, visualizer_id):
    print("selected visualizer: " + str(visualizer_id))
    # TODO: handle visualizer change
    return HttpResponseRedirect(reverse("index"))


def visualize(request, id):
    app_config = apps.get_app_config("graph_visualizer")
    plugins_visualization = app_config.plugins_visualization
    visualization = None
    for plugin in plugins_visualization:
        if plugin.get_identifier() == id:
            visualization = plugin.visualize(app_config.graph)
            break

    return render(
        request,
        "index.html",
        {
            "simple_visualizer": visualization,
        },
    )
