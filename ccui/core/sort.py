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
from .util import update_querystring



DIRECTIONS = set(["asc", "desc"])
DEFAULT = "asc"



def from_request(request, defaultfield=None, defaultdirection=DEFAULT):
    """
    Given a request, return tuple (sortfield, sortdirection).

    """
    sortfield = request.GET.get("sortfield", defaultfield)
    sortdirection = request.GET.get("sortdirection", defaultdirection)
    return sortfield, sortdirection


class Sort(object):
    def __init__(self, url_path, field=None, direction=DEFAULT):
        """
        Accepts the full URL path of the current request (including
        querystring), the current sort field name, and the current sort
        direction.

        """
        self.url_path = url_path
        self.field = field
        self.direction = direction


    def url(self, field):
        """
        Return a url for switching the sort to the given field name.

        """
        direction = DEFAULT
        if field == self.field:
            direction = toggle(self.direction)
        return url(self.url_path, field, direction)


    def dir(self, field):
        """
        Return the current sort direction for the given field: asc, desc, or
        empty string if this isn't the field sorted on currently.

        """
        if field == self.field:
            return self.direction
        return ""



def url(url, field, direction):
    return update_querystring(url, sortfield=field, sortdirection=direction)



def toggle(direction):
    return DIRECTIONS.difference([direction]).pop()
