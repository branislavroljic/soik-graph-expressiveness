from django.http import HttpResponse
from django.apps.registry import apps
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the graph index.")

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