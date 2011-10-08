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
from mock import Mock
from unittest2 import TestCase

from ..utils import Url



class TestFromRequest(TestCase):
    @property
    def func(self):
        from ccui.core.sort import from_request
        return from_request


    def _check(self, result, GET, *args):
        request = Mock()
        request.GET = GET
        self.assertEqual(self.func(request, *args), result)


    def test_implicit_defaults(self):
        self._check((None, "asc"), {})


    def test_given_defaults(self):
        self._check(("name", "desc"), {}, "name", "desc")


    def test_set(self):
        self._check(
            ("name", "desc"), {"sortfield": "name", "sortdirection": "desc"})



class TestSort(TestCase):
    @property
    def cls(self):
        from ccui.core.sort import Sort
        return Sort


    def test_attributes(self):
        s = self.cls("path", "name", "desc")
        self.assertEqual(s.field, "name")
        self.assertEqual(s.direction, "desc")


    def test_attribute_defaults(self):
        s = self.cls("path")
        self.assertEqual(s.field, None)
        self.assertEqual(s.direction, "asc")


    def test_url_same_field(self):
        s = self.cls("path", "name", "asc")
        self.assertEqual(
            s.url("name"), "path?sortfield=name&sortdirection=desc")


    def test_url_other_field(self):
        s = self.cls("path", "name", "asc")
        self.assertEqual(
            s.url("status"), "path?sortfield=status&sortdirection=asc")


    def test_dir_same_field(self):
        s = self.cls("path", "name", "asc")
        self.assertEqual(
            s.dir("name"), "asc")


    def test_dir_other_field(self):
        s = self.cls("path", "name", "asc")
        self.assertEqual(
            s.dir("status"), "")



class TestUrl(TestCase):
    @property
    def func(self):
        from ccui.core.sort import url
        return url


    def test_basic(self):
        self.assertEqual(
            Url(self.func("http://fake.base/some/", "name", "asc")),
            Url("http://fake.base/some/?sortfield=name&sortdirection=asc"))


    def test_override(self):
        self.assertEqual(
            Url(self.func(
                "http://fake.base/some/?sortfield=status&sortdirection=desc",
                "name", "asc")),
            Url("http://fake.base/some/?sortfield=name&sortdirection=asc"))


    def test_other(self):
        self.assertEqual(
            Url(self.func("http://fake.base/some/?blah=foo", "name", "asc")),
            Url("http://fake.base/some/?blah=foo&sortdirection=asc&sortfield=name"))


    def test_override_with_other(self):
        self.assertEqual(
            Url(self.func(
                "http://fake.base/?b=f&sortfield=status&sortdirection=desc",
                "name", "asc")),
            Url("http://fake.base/?sortfield=name&sortdirection=asc&b=f"))



class TestToggle(TestCase):
    @property
    def func(self):
        from ccui.core.sort import toggle
        return toggle


    def test_asc(self):
        self.assertEqual(self.func("asc"), "desc")


    def test_desc(self):
        self.assertEqual(self.func("desc"), "asc")
