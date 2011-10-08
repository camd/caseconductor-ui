# Case Conductor is a Test Case Management system.
# Copyright (C) 2011 uTest Inc.
# 
# This file is part of Case Conductor.
# 
# Case Conductor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Case Conductor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.
import json

from django.core.validators import URLValidator, ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response, redirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from django.contrib import messages

from ..core import decorators as dec
from ..relatedbugs.models import ExternalBug, ExternalBugList
from ..static.status import TestRunStatus, TestCycleStatus
from ..testexecution.models import TestRunIncludedTestCaseList
from ..users.decorators import login_redirect

from .finder import RunTestsFinder
from .models import TestCycleList, TestRunList, TestResultList



@login_redirect
@dec.finder(RunTestsFinder)
def home(request):
    return TemplateResponse(
        request,
        "runtests/home.html",
        {}
        )



@login_redirect
def finder_environments(request, run_id):
    run = TestRunList.get_by_id(run_id, auth=request.auth)

    return TemplateResponse(
        request,
        "runtests/_environment_form.html",
        {"testrun": run,
         })



@never_cache
@login_redirect
@dec.finder(RunTestsFinder)
@dec.paginate("cases")
def runtests(request, testrun_id):
    # force the CSRF cookie to be set
    # @@@ replace with ensure_csrf_cookie decorator in Django 1.4
    get_token(request)

    testrun = TestRunList.get_by_id(testrun_id, auth=request.auth)

    if not testrun.environmentgroups_prefetch.match(request.environments):
        return redirect("runtests_environment", testrun_id=testrun_id)

    cycle = testrun.testCycle
    product = cycle.product

    # for prepopulating finder
    cycles = TestCycleList.ours(auth=request.auth).sort("name", "asc").filter(
        product=product, status=TestCycleStatus.ACTIVE)
    runs = TestRunList.ours(auth=request.auth).sort("name", "asc").filter(
        testCycle=cycle, status=TestRunStatus.ACTIVE)

    return TemplateResponse(
        request,
        "runtests/run.html",
        {"product": product,
         "cycle": cycle,
         "testrun": testrun,
         "cases": TestRunIncludedTestCaseList.get(auth=request.auth).filter(
                testRun=testrun),
         "finder": {
                "cycles": cycles,
                "runs": runs,
                },
         })


ACTIONS = {
    "start": [],
    "finishsucceed": [],
    "finishinvalidate": ["comment"],
    "finishfail": ["failedStepNumber", "actualResult"],
    }


@login_redirect
@require_POST
def result(request, result_id):
    result = TestResultList.get_by_id(result_id, auth=request.auth)

    action = request.POST.get("action", None)
    try:
        argnames = ACTIONS[action]
    except KeyError:
        return HttpResponseBadRequest(
            "%s is not a valid result action." % action)

    kwargs = {"auth": request.auth}

    for argname in argnames:
        try:
            kwargs[argname] = request.POST[argname]
        except KeyError:
            return HttpResponseBadRequest(
                "Required parameter %s missing." % argname)

        if not kwargs[argname]:
            messages.error(request, "The %r field is required." % argname)
            return json_response({})

    getattr(result, action)(**kwargs)

    new_bug_url = request.POST.get("related_bug", None)
    if new_bug_url:
        try:
            URLValidator()(new_bug_url)
        except ValidationError:
            messages.error(request, "The bug URL must be a valid URL.")
            return json_response({})
        bug = ExternalBug(url=new_bug_url, externalIdentifier="1")
        result.relatedbugs.post(bug)
    else:
        for bug_id in request.POST.getlist("bugs"):
            if bug_id:
                bug = ExternalBugList.get_by_id(bug_id, auth=request.auth)
                result.relatedbugs.post(bug)

    return render_to_response(
        "runtests/_run_case.html",
        {"case": result.testCase,
         "caseversion": result.testCaseVersion,
         "result": result,
         "open": action == "start",
         })


def json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")
