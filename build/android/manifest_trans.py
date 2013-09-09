#!/usr/bin/env python

# Copyright (c) 2013 Intel Corporation. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Transact json-format manifest configuration file and 
# provide the fields, which have to be integrated with 
# Android packaging tool (make_apk) to generate AndroidManifest.xml

# Sample usage from shell script:
# manifest_trans.py --jsonfile=manifest.json

import json
import optparse
import os
import sys
import traceback


class TransWrtManifest(object):
  """ The class is sued to parse crosswalk runtime model manifest json-format 
  Args:
    input_path: the full path of the manifest json file
  """
  def __init__(self, input_path):
    self.input_path = input_path
    input_file = file(self.input_path)
    try:
      input_src = input_file.read()
      self.data_src = json.JSONDecoder().decode(input_src)
    except IOError:
      traceback.print_exc()
    finally:
      input_file.close()

  def OutputItems(self):
    """ The manifest field items are reorganized and returned as a dictionary
    support single or multiple values of keys
    Returns:
      A dictionary to the corresponding items. the dictionary keys are described
      as follows, the value is set to "" if the value of the key is not set 
    package_name:     package
    app_name:         used as apk
    app_version:      application
    icon_path:        the path of icon
    app_url:          the url of application, e.g. hosted
    app_root:         the root path of the web
                      this flag allows to package local web app as apk.
    app_local_path:   the relative path of entry file based on |app_root|
                      this flag should work with "--app-root" together. 
    required_version: the required crosswalk runtime version
    plugin:           the plug-in path and file name
    fullscree:        the fullscreen flag of the application
    """                
    ret_dict = {}
    ret_dict['package_name'] = "com.crosswalk.app." + self.data_src['name']
    ret_dict['app_name'] = self.data_src['name']
    ret_dict['app_version'] = self.data_src['version']
    file_path_prefix = os.path.split(self.input_path)[0]
    origin_icon_path = os.path.join(file_path_prefix,'src')
    # get the icon relative path
    for key in self.data_src['icons']:
      icon_rel_path = (os.path.split(self.data_src['icons'][key]))[0]
      if (len(icon_rel_path) != 0):
        icon_path = os.path.join(origin_icon_path, icon_rel_path)
      else:
        icon_path = origin_icon_path
    ret_dict['icon_path'] = icon_path
    app_root = file_path_prefix
    app_url = self.data_src['launch_path']
    if "http" in app_url.lower():
      app_local_path = ""
    else:
      app_local_path = app_url
      app_url = ""
    ret_dict['app_url'] = app_url
    ret_dict['app_root'] = app_root
    ret_dict['app_local_path'] = app_local_path
    ret_dict['required_version'] = self.data_src['required_version']
    ret_dict['plugin'] = self.data_src['plugin']
    ret_dict['fullscreen'] = self.data_src['fullscreen']
    return ret_dict
    
  # Show values
  def ShowItems(self, ret_dict):
    print("package_name: %s" % ret_dict['package_name'])
    print("app_name: %s" % ret_dict['app_name'])
    print("app_version: %s" % ret_dict['app_version'])
    print("icon_path: %s" % ret_dict['icon_path'])  
    print("app_url: %s" % ret_dict['app_url'])
    print("app_root: %s" % ret_dict['app_root'])
    print("app_local_path: %s" % ret_dict['app_local_path'])
    print("required_version: %s" % ret_dict['required_version'])
    print("plugin: %s" % ret_dict['plugin'])      
    print("fullscreen: %s" % ret_dict['fullscreen'])      
    

def main():
  parser = optparse.OptionParser()
  info = ('The input json-format file name. Such as: '
          '-j manifest.json')
  parser.add_option('-j', action = "store", dest = "jsonfile", help = info)
  info = ('The input json-format file name. Such as: '
          '--jsonfile=manifest.json')
  parser.add_option('--jsonfile', action = "store", dest = "jsonfile", 
                   help = info)

  opts, args = parser.parse_args()
  try:
    JsonParser = TransWrtManifest(opts.jsonfile)
    ret_dict = JsonParser.OutputItems()
    JsonParser.ShowItems(ret_dict)
  except SystemExit, ec:
    print 'Exiting with error code: %d' % ec.code
    return ec.code
  return 0

if __name__ == '__main__':
  sys.exit(main())
