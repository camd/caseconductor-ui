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
from mock import patch, Mock
from unittest2 import TestCase


from ..utils import creds



class TestNonFieldErrorsClassFormMixin(TestCase):
    @property
    def mixin(self):
        from ccui.core.forms import NonFieldErrorsClassFormMixin
        return NonFieldErrorsClassFormMixin


    @property
    def form_class(self):
        from django import forms

        class PersonForm(self.mixin, forms.Form):
            name = forms.CharField()
            age = forms.IntegerField()

            def clean(self):
                if (self.cleaned_data.get("name") == "Shakespeare" and
                    self.cleaned_data.get("age", 0) < 400):
                    raise forms.ValidationError("Too young to be Shakespeare.")

        return PersonForm


    def test_non_field_errorlist(self):
        form = self.form_class({"name": "Shakespeare", "age": "25"})

        nfe = form.non_field_errors()

        self.assertTrue('class="errorlist nonfield"' in unicode(nfe))


    def test_field_errorlist(self):
        form = self.form_class({"name": "Joe"})

        fe = unicode(form["age"].errors)

        self.assertTrue('class="' in fe)
        self.assertFalse("nonfield" in fe)


    def test_no_nonfield_errors(self):
        form = self.form_class({"name": "Joe", "age": "25"})

        self.assertEqual(unicode(form.non_field_errors()), u"")



class RemoteObjectFormTest(TestCase):
    @property
    def form_class(self):
        import floppyforms as forms
        from ccui.core.forms import RemoteObjectForm

        class PersonForm(RemoteObjectForm):
            name = forms.CharField()
            birthday = forms.DateField()

        return PersonForm


    def test_datefield_placeholder(self):
        self.assertEqual(
            self.form_class().fields["birthday"].widget.attrs["placeholder"],
            "yyyy-mm-dd")



class AddEditFormTest(TestCase):
    @property
    def form_class(self):
        from ccui.core.forms import AddEditForm
        return AddEditForm


    @patch("ccui.core.forms.errors.error_message_and_fields")
    def test_non_field_errors_dont_pass_silently(self, emaf):
        emaf.return_value = ("unknown error", [])
        obj, err = ("fake obj", "fake err")

        f = self.form_class(auth="auth")

        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            f.handle_error(obj, err)

        emaf.assert_called_once_with(obj, err)


    def test_no_edit_fields(self):
        import floppyforms as forms

        class PersonForm(self.form_class):
            name = forms.CharField()
            age = forms.CharField()

            no_edit_fields = ["age"]

        f = PersonForm(instance=Mock(), auth=Mock())

        self.assertEqual(f.fields["age"].read_only, True)


    def test_add_no_save_with_error(self):
        import floppyforms as forms

        class PersonForm(self.form_class):
            entryclass = Mock()
            listclass = Mock()

            name = forms.CharField(required=True)
            birthdate = forms.DateField(required=False)

        # bad date will fail validation
        f = PersonForm(
            data={"name": "Someone", "birthdate": "2011-12-32"},
            auth=creds("admin@example.com"),
            )

        self.assertFalse(f.is_valid())

        # failed validation should mean new obj is never instantiated
        self.assertEqual(PersonForm.entryclass.call_count, 0)


    def test_edit_no_save_with_error(self):
        import floppyforms as forms

        class PersonForm(self.form_class):
            name = forms.CharField(required=True)
            birthdate = forms.DateField(required=False)

        instance = Mock()

        # bad date will fail validation
        f = PersonForm(
            data={"name": "Someone", "birthdate": "2011-12-32"},
            instance=instance,
            auth=creds("admin@example.com"),
            )

        self.assertFalse(f.is_valid())

        # failed validation should mean obj is never saved
        self.assertEqual(instance.put.call_count, 0)



class BareTextareaTest(TestCase):
    def test_no_attrs(self):
        from ccui.core.forms import BareTextarea
        self.assertEqual(BareTextarea().attrs, {})



class ReadOnlyWidgetTest(TestCase):
    @property
    def widget(self):
        from ccui.core.forms import ReadOnlyWidget
        return ReadOnlyWidget


    def test_simple(self):
        self.assertEqual(
            self.widget().render("name", "value"),
            u'value<input type="hidden" name="name" value="value">\n'
            )


    def test_attrs(self):
        self.assertEqual(
            self.widget().render("name", "value", {"attr": "val"}),
            u'value<input type="hidden" name="name" value="value" attr="val">\n'
            )


    def test_choices(self):
        widget = self.widget()
        widget.choices = [(1, "one"), (2, "two")]
        self.assertEqual(
            widget.render("name", 1),
            u'one<input type="hidden" name="name" value="1">\n'
            )


    def test_choices_bad_choice(self):
        widget = self.widget()
        widget.choices = [(1, "one"), (2, "two")]
        self.assertEqual(
            widget.render("name", 3),
            u'3<input type="hidden" name="name" value="3">\n'
            )


    def test_choices_iterator(self):
        widget = self.widget()
        widget.choices = (i for i in [(1, "one"), (2, "two")])
        self.assertEqual(
            widget.render("name", 2),
            u'two<input type="hidden" name="name" value="2">\n'
            )


    def test_choices_extra_data(self):
        widget = self.widget()
        widget.choices = [(1, "one", "extra"), (2, "two", "extra")]
        self.assertEqual(
            widget.render("name", 1),
            u'one<input type="hidden" name="name" value="1">\n'
            )
