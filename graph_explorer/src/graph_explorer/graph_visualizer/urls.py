from django.urls import path
from . import views

urlpatterns = [
    path("", 
         views.index, 
         name="index"),
    path("workspaces/<int:workspace_id>", 
         views.workspace, 
         name="workspace"),
    path(
        "workspaces/add",
        views.add_workspace,
        name="add_workspace",
    ),
    path(
        "workspaces/delete/<int:workspace_id>",
        views.delete_workspace,
        name="delete-workspace",
    ),
    path(
        "visualizers/<str:visualizer_id>",
        views.select_visualizer,
        name="visualizer",
    ),
    path(
        "workspaces/<int:workspace_id>/filter",
        views.filter,
        name="filter",
    ),
    path(
        "workspaces/<int:workspace_id>/search",
        views.search,
        name="search",
    ),
    path(
        "workspaces/<int:workspace_id>/reset",
        views.reset,
        name="reset",
    )
]
