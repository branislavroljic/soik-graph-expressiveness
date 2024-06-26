from django.apps.registry import apps
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse

from platform_soik.config import PlatformConfig
from platform_soik.models import Workspace



platform_config: PlatformConfig = apps.get_app_config(
    "graph_visualizer"
).get_platform_config()


# Create your views here.
def index(request):
    return render(request, "index.html", platform_config.get_context())


def workspace(request, workspace_id):

    if workspace_id not in list(map(lambda ws: ws.id, platform_config.workspaces)):
        return HttpResponseNotFound("Workspace not found.")

    platform_config.select_workspace(workspace_id)

    context = platform_config.get_context()

    return render(request, "index.html", context=context)


def select_visualizer(_, visualizer_id):
    # print("selected visualizer: " + str(visualizer_id))
    platform_config.current_workspace.set_visualizer_plugin(visualizer_id=visualizer_id)
    return HttpResponse()


def add_workspace(request):

    form_data = request.POST.dict()
    print(form_data)
    # data_sources_ids = get_data_sources_ids()
    data_source_id = form_data.get("ws-data-source")
    # if data_source_id is None:
    #     datasource_name = data_sources[0]

    workspace_name = form_data.get("ws-name")
    # del form_data["workspace-name"]
    # del form_data["csrfmiddlewaretoken"]

    file = request.FILES.get("ws-data-source-file")

    # try:
    new_workspace = Workspace()
    new_workspace.name = workspace_name
    new_workspace.file = file
    new_workspace.set_data_source_plugin(data_source_id)
    new_workspace.set_visualizer_plugin("simple_graph_visualizer")
    # except Exception as e:
    #     return HttpResponse(f"Error: {str(e)}", status=400)

    platform_config.add_workspace(new_workspace)

    # return HttpResponseRedirect(
    #     reverse("workspace", kwargs={"workspace_id": new_workspace.id})
    # )
    return JsonResponse({"workspace_id": new_workspace.id})


def delete_workspace(self, workspace_id):
    platform_config.delete_workspace(workspace_id)
    return HttpResponseRedirect(reverse("index"))


def filter(request, workspace_id ):    
    params = {}
    params['filter_value'] = request.GET.get('filter_value') 
    params['filter_operator'] = request.GET.get('filter_operator') 
    params['filter_attribute'] = request.GET.get('filter_attribute')
    current_workspace = platform_config.select_workspace(workspace_id)
    current_workspace.filter_params = params
    current_workspace.filter_graph()
    return HttpResponse()

def search(request, workspace_id):

    search_word = request.GET.get('src')    
    current_workspace = platform_config.select_workspace(workspace_id)
    current_workspace.search_param = search_word
    current_workspace.search_graph()
    return HttpResponse()


def reset(_, workspace_id):
    current_workspace = platform_config.select_workspace(workspace_id)
    current_workspace.reset_graph()
    return HttpResponse()


# def get_data_sources_ids() -> list:
#     loaders: list[Parser] = apps.get_app_config("graph_visualizer").plugins_loader

#     return list(map(lambda ds: ds.get_identifier(), loaders))
