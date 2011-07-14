from functools import wraps
import json

from django.contrib import messages
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string

from ..core import errors
from ..core.util import get_action
from ..environments.models import (
    EnvironmentType, EnvironmentTypeList, EnvironmentList, Environment)



ACTION_TYPES = {
    "category": (
        EnvironmentTypeList,
        "manage/environment/add_profile/_category_list_item.html",
        ),
    "element": (
        EnvironmentList,
        "manage/environment/add_profile/_element_list_item.html",
        ),
    }



def environment_actions():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.is_ajax() and request.method == "POST":
                data = {}

                action_data = get_action(request.POST)
                if action_data:
                    action, obj_spec = action_data
                    if action in ["delete"]:
                        obj_type, obj_id = obj_spec.split("-")
                        list_obj, template_name = ACTION_TYPES[obj_type]
                        obj = list_obj.get_by_id(obj_id, auth=request.auth)

                        try:
                            getattr(obj, action)()
                        except obj.Conflict, e:
                            messages.error(
                                request, errors.error_message(obj, e))
                            success = False
                        else:
                            success = True

                        if action == "delete":
                            if success:
                                data["html"] = ""
                            else:
                                data["no_replace"] = True
                        else:
                            data["html"] = render_to_string(
                                template_name,
                                {obj_type: obj},
                                RequestContext(request))
                elif "new-category-name" in request.POST:
                    template_name = ACTION_TYPES["category"][1]
                    new_category_name = request.POST.get("new-category-name")
                    et = EnvironmentType(
                        name=new_category_name,
                        company=request.company,
                        groupType=False)
                    EnvironmentTypeList.get(auth=request.auth).post(et)

                    data["html"] = render_to_string(
                        template_name,
                        {"category": et},
                        RequestContext(request))
                elif "new-element-name" in request.POST:
                    template_name = ACTION_TYPES["element"][1]
                    preview_template_name = (
                        "manage/environment/add_profile/"
                        "_element_preview_list_item.html")

                    e = Environment(
                        name=request.POST.get("new-element-name"),
                        company=request.company,
                        environmentType=request.POST.get("category-id"))
                    EnvironmentList.get(auth=request.auth).post(e)

                    data["elem"] = render_to_string(
                        template_name,
                        {"element": e},
                        RequestContext(request))

                    data["preview"] = render_to_string(
                        preview_template_name,
                        {"element": e},
                        RequestContext(request))

                return HttpResponse(
                    json.dumps(data), content_type="application/json")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator