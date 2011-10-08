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
from flufl.enum import Enum
from mock import patch
from unittest2 import TestCase

from ..core.test_fields import BaseFieldTests



class SomeStatus(Enum):
    DRAFT = 1
    ACTIVE = 2



class StatusValueTest(TestCase):
    def _make(self, val):
        from ccui.static.fields import StatusValue
        return StatusValue(val)


    def test_true(self):
        self.assertIs(self._make(SomeStatus.DRAFT).DRAFT, True)


    def test_false(self):
        self.assertIs(self._make(SomeStatus.DRAFT).ACTIVE, False)


    def test_error(self):
        with self.assertRaises(AttributeError):
            self._make(SomeStatus.DRAFT).BLAH


    def test_repr(self):
        self.assertEqual(
            repr(self._make(SomeStatus.DRAFT)),
            "StatusValue(<EnumValue: SomeStatus.DRAFT [int=1]>)")


    def test_str(self):
        self.assertEqual(str(self._make(SomeStatus.DRAFT)), "Draft")


    def test_unicode(self):
        self.assertEqual(unicode(self._make(SomeStatus.DRAFT)), u"Draft")



class FakeCodeValue(object):
    def __init__(self, id_, description):
        self.id = id_
        self.description = description



@patch("ccui.static.fields.STATUS_ENUMS_BY_KEY", {"SOMESTATUS": SomeStatus})
@patch("ccui.static.fields.get_codevalue",
       lambda key, id_: {
        1: FakeCodeValue(1, "Draft"),
        2: FakeCodeValue(2, "Active")
        }.get(id_))
class StaticDataTest(BaseFieldTests):
    @property
    def field_cls(self):
        from ccui.static.fields import StaticData
        return StaticData


    prepend_args = ("SOMESTATUS",)


    def test_encode(self):
        f = self.field()

        self.assertEqual(f.encode(SomeStatus.DRAFT), "1")


    def test_encode_string(self):
        f = self.field()

        self.assertEqual(f.encode("1"), "1")


    def test_encode_nonint_string(self):
        f = self.field()

        self.assertEqual(f.encode("blah"), "blah")


    def test_encode_int(self):
        f = self.field()

        self.assertEqual(f.encode(1), "1")


    def test_encode_none(self):
        f = self.field()

        self.assertEqual(f.encode(None), None)


    def test_encode_statusvalue(self):
        from ccui.static.fields import StatusValue
        f = self.field()

        self.assertEqual(f.encode(StatusValue(SomeStatus.DRAFT)), "1")


    def test_encode_codevalue(self):
        from ccui.static.models import CodeValue
        f = self.field()

        self.assertEqual(f.encode(CodeValue(id="1")), "1")


    def test_default_names(self):
        f = self.field()

        self.assertEqual(f.api_name, "ns1.attnameId")
        self.assertEqual(f.api_filter_name, "attnameId")
        self.assertEqual(f.api_submit_name, "attnameId")


    def test_set_api_name(self):
        f = self.field(api_name="apiname")

        self.assertEqual(f.api_name, "ns1.apiname")
        self.assertEqual(f.api_filter_name, "apinameId")
        self.assertEqual(f.api_submit_name, "apinameId")


    def test_set_api_submit_name(self):
        f = self.field(api_submit_name="apisubmitname")

        self.assertEqual(f.api_name, "ns1.attnameId")
        self.assertEqual(f.api_filter_name, "attnameId")
        self.assertEqual(f.api_submit_name, "apisubmitname")


    def test_set_api_name_and_api_submit_name(self):
        f = self.field(api_name="apiname", api_submit_name="apisubmitname")

        self.assertEqual(f.api_name, "ns1.apiname")
        self.assertEqual(f.api_filter_name, "apinameId")
        self.assertEqual(f.api_submit_name, "apisubmitname")


    def test_submit(self):
        f, cls = self.field_and_cls()
        self.assertEqual(
            f.submit_data(
                cls(attname=SomeStatus.ACTIVE)), {"attnameId": "2"})


    def test_get_descriptor(self):
        f, cls = self.field_and_cls()
        self.assertIs(cls.attname, f)


    def test_get_statusvalue(self):
        from ccui.static.fields import StatusValue

        f, cls = self.field_and_cls()

        val = cls(attname=1).attname
        self.assertIsInstance(val, StatusValue)
        self.assertEqual(str(val), "Draft")


    def test_get_no_states(self):
        f, cls = self.field_and_cls()

        f.states = None

        val = cls(attname=1).attname
        self.assertIsInstance(val, FakeCodeValue)
        self.assertEqual(val.description, "Draft")
