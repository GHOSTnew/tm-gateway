#!/usr/bin/env python

# Copyleft 2014 GHOSTnew
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


def IPisBanned(IP):
    try:
        IPlist = open('conf/Banlist.txt')
    except IOError:
        return False

    for addrIP in IPlist:
        addrIP = addrIP.replace("\n", "").split(" ")[0]
        if addrIP == IP:
            IPlist.close()
            return True
    IPlist.close()
    return False


def getReason(IP):
    try:
        IPlist = open('conf/Banlist.txt')
    except IOError:
        return ""

    for line in IPlist:
        line = line.replace("\n", "").split(" ")
        addrIP = line[0]
        if addrIP == IP:
            reason = ""
            if len(line) > 1:
                for i in range(1, len(line)):
                    if i == 1:
                        reason = line[i]
                    else:
                        reason += " " + line[i]
            IPlist.close()
            return reason
    IPlist.close()
    return ""
