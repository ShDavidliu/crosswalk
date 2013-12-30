#!/usr/bin/env python

# Copyright (c) 2013, 2014 Intel Corporation. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Provide the function interface of mapping the permissions
from manifest.json to AndroidManifest.xml.
It suppports the mapping of permission fields both defined in Crosswalk
and supported by Android Manifest specification.

Sample usage from shell script:
python permissions_mapping.py --jsonfile=/path/to/manifest.json
--manifest=/path/to/AndroidManifest.xml
"""

import optparse
import os
import sys

from manifest_json_parser import ManifestJsonParser
from xml.dom import minidom
from xml.parsers.expat import ExpatError

# The global permission mapping table.
__all__ = {
  'alarm'                       : ['com.android.alarm.permission.SET_ALARM'],
  'battery'                     : ['android.permission.BATTERY_STATS'],
  'bluetooth'                   : ['android.permission.BLUETOOTH',
                                   'android.permission.BLUETOOTH_ADMIN'],
  'browser'                     : ['com.android.browser.permission.'
                                   'READ_HISTORY_BOOKMARKS',
                                   'com.android.browser.permission.'
                                   'WRITE_HISTORY_BOOKMARKS'],
  'calendar'                    : ['android.permission.READ_CALENDAR',
                                   'android.permission.WRITE_CALENDAR'],
  'contacts'                    : ['android.permission.READ_CONTACTS',
                                   'android.permission.WRITE_CONTACTS'],
  'geolocation'                 : ['android.permission.ACCESS_COARSE_LOCATION',
                                   'android.permission.ACCESS_FINE_LOCATION',
                                   'android.permission.'
                                   'ACCESS_LOCATION_EXTRA_COMMANDS',
                                   'android.permission.ACCESS_MOCK_LOCATION',
                                   'android.permission.'
                                   'CONTROL_LOCATION_UPDATES',
                                   'android.permission.'
                                   'INSTALL_LOCATION_PROVIDER',
                                   'android.permission.LOCATION_HARDWARE'],
  'messaging'                   : ['android.permission.READ_SMS',
                                   'android.permission.SEND_SMS',
                                   'android.permission.WRITE_SMS'],
  'networkinformation'          : ['android.permission.ACCESS_NETWORK_STATE',
                                   'android.permission.ACCESS_WIFI_STATE',
                                   'android.permission.CHNANGE_NETWORK_STATE',
                                   'android.permission.'
                                   'CHNANGE_WIFI_MULTICAST_STATE',
                                   'android.permission.CHNANGE_WIFI_STATE'],
  'rawsockets'                  : ['android.permission.INTERNET'],
  'screenorientation'           : ['android.permission.SET_ORIENTATION'],
  'secureelement'               : ['android.permission.WRITE_SECURE_SETTINGS'],
  'systemsettings'              : ['android.permission.WRITE_SETTINGS'],
  'telephony'                   : ['android.permission.MODIFY_PHONE_STATE'],
  'vibration'                   : ['android.permission.VIBRATE']
}


#TODO: add the corresponding permission if related API is implemented.
fully_supported_permissions = ['contacts', 'geolocation']


partly_supported_permissions = ['messaging']


def AddElementAttribute(doc, node, name, value):
  root = doc.documentElement
  item = doc.createElement(node)
  item.setAttribute(name, value)
  root.appendChild(item)


def HandlePermissions(options, xmldoc):
  """ Implement the mapping of permission list to the AndroidManifest.xml file.
  Args:
    options: the parsed options with permissions.
    xmldoc: the parsed xmldoc of the AndroidManifest.xml file, used for
        reading and writing.
  """
  if options.permissions:
    existing_permission_list = []
    used_permissions = xmldoc.getElementsByTagName("uses-permission")
    for item in used_permissions:
      existing_permission_list.append(item.getAttribute("android:name"))

    for permission in options.permissions.split(':'):
      if permission.lower() not in \
          fully_supported_permissions + partly_supported_permissions:
        print 'Error: \'%s\' related API is not supported currently.' \
            % permission
        sys.exit(1)
      if permission.lower() in partly_supported_permissions:
        print 'Warning: \'%s\' is partly supported.' % permission
      permission_item = __all__.get(permission.lower())
      if permission_item:
        for android_permission in permission_item:
          if android_permission not in existing_permission_list:
            AddElementAttribute(xmldoc, 'uses-permission',
                                'android:name', android_permission)


def main():
  """Respond to command mode of the mapping permission list."""
  parser = optparse.OptionParser()
  info = ('The input json-format file name. Such as: '
          '--jsonfile=manifest.json')
  parser.add_option('-j', '--jsonfile', action='store', dest='jsonfile',
                    help=info)
  info = ('The destination android manifest file name. Such as: '
          '--manifest=AndroidManifest.xml')
  parser.add_option('-m', '--manifest', action='store', dest='manifest',
                    help=info)
  options, _ = parser.parse_args()
  if not options.jsonfile:
    print 'Please set the manifest.json file.'
    return 1
  if not options.manifest:
    print 'Please set the AndroidManifest.xml file.'
    return 1
  try:
    json_parser = ManifestJsonParser(os.path.expanduser(options.jsonfile))
    if json_parser.GetPermissions():
      options.permissions = json_parser.GetPermissions()
  except SystemExit, ec:
    print 'Exiting with error code: %d' % ec.code
    return ec.code
  try:
    xmldoc = minidom.parse(options.manifest)
    HandlePermissions(options, xmldoc)
    file_handle = open(options.manifest, 'wb')
    xmldoc.writexml(file_handle)
    file_handle.close()
  except (ExpatError, IOError):
    print 'There is an error in AndroidManifest.xml.'
    return 1
  return 0


if __name__ == '__main__':
  sys.exit(main())
