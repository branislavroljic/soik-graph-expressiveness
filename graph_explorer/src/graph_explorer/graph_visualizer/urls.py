from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("workspaces/<int:workspace_id>", views.workspace, name="workspace"),
    path(
        "visualizers/<int:visualizer_id>",
        views.select_visualizer,
        name="visualizer",
    ),
    path("visualization/plugin/<str:id>", views.visualize, name="visualization_plugin"),
    # path("visualization/plugin/<str:id>", views.visualize, name="visualization_plugin"),
    # # path("loading/plugin/<str:id>", views.load, name="visualization_plugin"),
    # path("home/", views.home, name="index-view"),
]
