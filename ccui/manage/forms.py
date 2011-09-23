"""
Case Conductor is a Test Case Management system.
Copyright (C) 2011 uTest Inc.

This file is part of Case Conductor.

Case Conductor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Case Conductor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.

"""
from django.core.exceptions import ValidationError

import floppyforms as forms

from ..core import forms as ccforms

from ..products.models import Product, ProductList
from ..testcases.bulk import BulkParser
from ..testcases.forms import StepFormSet
from ..testcases.models import (
    TestSuite, TestSuiteList, TestCaseVersion, TestCaseList, TestCaseStep)
from ..testexecution.models import (
    TestCycle, TestCycleList, TestRun, TestRunList)



def product_id_attrs(obj):
    return {"data-product-id": obj.product.id}



class ProductForm(ccforms.AddEditForm):
    name = forms.CharField()
    description = forms.CharField(widget=ccforms.BareTextarea)
    team = ccforms.ModelMultipleChoiceField(required=False)


    assign_later = ["team", "profile"]
    entryclass = Product
    listclass = ProductList


    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop("company")
        if "instance" not in kwargs:
            self.base_fields["profile"] = ccforms.ModelChoiceField()

        super(ProductForm, self).__init__(*args, **kwargs)


    @property
    def extra_creation_data(self):
        return {"company": self.company}



class TestCycleForm(ccforms.AddEditForm):
    name = forms.CharField()
    description = forms.CharField(widget=ccforms.BareTextarea)
    product = ccforms.ModelChoiceField()
    start_date = forms.DateField()
    end_date = forms.DateField(required=False)
    team = ccforms.ModelMultipleChoiceField(required=False)


    no_edit_fields = ["product"]
    field_mapping = {
        "start_date": "startDate",
        "end_date": "endDate"}
    assign_later = ["team"]
    entryclass = TestCycle
    listclass = TestCycleList
    extra_creation_data = {
        "communityAccessAllowed": True,
        "communityAuthoringAllowed": True,
        }



class TestRunForm(ccforms.AddEditForm):
    name = forms.CharField()
    description = forms.CharField(widget=ccforms.BareTextarea)
    test_cycle = ccforms.ModelChoiceField(
        option_attrs=product_id_attrs)
    start_date = forms.DateField()
    end_date = forms.DateField(required=False)
    team = ccforms.ModelMultipleChoiceField(required=False)
    suites = ccforms.ModelMultipleChoiceField(
        required=False, option_attrs=product_id_attrs)


    no_edit_fields = ["test_cycle"]
    field_mapping = {
        "test_cycle": "testCycle",
        "start_date": "startDate",
        "end_date": "endDate"}
    assign_later = ["team", "suites"]
    entryclass = TestRun
    listclass = TestRunList
    extra_creation_data = {
        "selfAssignLimit": 0,
        "selfAssignAllowed": True,
        }



class TestSuiteForm(ccforms.AddEditForm):
    name = forms.CharField()
    description = forms.CharField(widget=ccforms.BareTextarea)
    product = ccforms.ModelChoiceField(
        option_attrs=lambda p: {"data-product-id": p.id})
    cases = ccforms.ModelMultipleChoiceField(
        required=False,
        label_from_instance=lambda c: c.name,
        option_attrs=product_id_attrs)


    no_edit_fields = ["product"]
    assign_later = ["cases"]
    entryclass = TestSuite
    listclass = TestSuiteList



class BulkTestCaseForm(ccforms.RemoteObjectForm):
    product = ccforms.ModelChoiceField()
    cases = forms.CharField(widget=ccforms.BareTextarea)


    def __init__(self, *args, **kwargs):
        product_choices = kwargs.pop("product_choices")

        self.auth = kwargs.pop("auth")

        super(BulkTestCaseForm, self).__init__(*args, **kwargs)

        self.fields["product"].obj_list = product_choices


    def clean_cases(self):
        parser = BulkParser()
        data = parser.parse(self.cleaned_data["cases"])

        for d in data:
            if "error" in d:
                raise ValidationError(d["error"])

        return data


    def clean(self):
        cases = []
        tcl = TestCaseList.get(auth=self.auth)

        for d in self.cleaned_data.get("cases", []):
            tcdata = dict(
                TestCaseForm.extra_creation_data,
                product=self.cleaned_data["product"],
                name=d["name"],
                description="\r\n".join(d["description"]),
                )

            tcv = TestCaseVersion(**tcdata)
            try:
                tcl.post(tcv)
            except TestCaseList.Conflict, e:
                for case in cases:
                    TestCaseList.get_by_id(
                        case.testCaseId, auth=self.auth).delete()
                self.handle_error(tcv, e)
                break

            cases.append(tcv)

            for i, stepdata in enumerate(d["steps"]):
                step = TestCaseStep(
                    stepNumber=i+1,
                    instruction="\n".join(stepdata["instruction"]),
                    expectedResult="\n".join(stepdata["expectedResult"]),
                    name="step %s" % str(i + 1),
                    testCaseVersion=tcv,
                    estimatedTimeInMin=0,
                    )

                tcv.steps.post(step)

        self.cases = cases

        return self.cleaned_data


    def save(self):
        return self.cases




class TestCaseForm(ccforms.AddEditForm):
    name = forms.CharField()
    description = forms.CharField()
    product = ccforms.ModelChoiceField()
    # @@@ tags = forms.CharField(required=False)


    no_edit_fields = ["product"]
    entryclass = TestCaseVersion
    listclass = TestCaseList
    extra_creation_data = {
        "maxAttachmentSizeInMbytes": 0,
        "maxNumberOfAttachments": 0,
        "automationUri": "",
        "description": "",
        }

    def create_formsets(self, *args, **kwargs):
        self.steps_formset = StepFormSet(
            *args, **dict(kwargs, prefix="steps"))

        super(TestCaseForm, self).create_formsets(*args, **kwargs)


    def is_valid(self):
        if self.steps_formset.is_valid():
            self.steps_formset_clear = True
            return super(TestCaseForm, self).is_valid()
        return False


    def clean(self):
        # If the formset is not valid, we don't want to actually try saving the
        # testcase.
        if not getattr(self, "steps_formset_clear", False):
            return self.cleaned_data
        return super(TestCaseForm, self).clean()


    def edit_clean(self):
        ret = super(TestCaseForm, self).edit_clean()

        # Name field can't be edited via TestCaseVersion, so we do it via the
        # TestCase proper
        tc = TestCaseList.get_by_id(self.instance.testCaseId, auth=self.auth)
        tc.name = self.instance.name = self.cleaned_data["name"]
        try:
            tc.put()
        except self.instance.Conflict, e:
            self.handle_error(self.instance, e)

        return ret



    def save(self):
        self.steps_formset.save(self.instance)

        return super(TestCaseForm, self).save()
