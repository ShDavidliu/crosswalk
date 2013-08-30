// Copyright (c) 2013 Intel Corporation. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef XWALK_EXTENSIONS_RENDERER_XWALK_EXTENSION_CLIENT_H_
#define XWALK_EXTENSIONS_RENDERER_XWALK_EXTENSION_CLIENT_H_

#include "base/memory/scoped_ptr.h"
#include "ipc/ipc_listener.h"
#include "ipc/ipc_sender.h"
#include "xwalk/extensions/renderer/xwalk_remote_extension_runner.h"

namespace xwalk {
namespace extensions {

// This class holds the JavaScript context of Extensions. It lives in the
// Render Process and communicates directly with its associated
// XWalkExtensionServer through an IPC channel.
class XWalkExtensionClient : public IPC::Listener, public IPC::Sender {
 public:
  XWalkExtensionClient(IPC::ChannelProxy* channel);
  virtual ~XWalkExtensionClient() {}

  // IPC::Listener Implementation.
  virtual bool OnMessageReceived(const IPC::Message& message) { return true; }

  // IPC::Sender Implementation.
  virtual bool Send(IPC::Message* msg);

  XWalkRemoteExtensionRunner* CreateRunner(
    XWalkExtensionRenderViewHandler* handler, int64_t frame_id,
    const std::string& extension_name,
    XWalkRemoteExtensionRunner::Client* client);

  // FIXME(jeez) make this private
  void OnRegisterExtension(const std::string& name, const std::string& api) {
    extension_apis_[name] = api;
  }

 private:
  IPC::ChannelProxy* channel_;

  typedef std::map<std::string, std::string> ExtensionAPIMap;
  ExtensionAPIMap extension_apis_;

  typedef std::map<int, XWalkRemoteExtensionRunner*> RunnersMap;
  RunnersMap runners_;

  int next_instance_id_;
};

}  // namespace extensions
}  // namespace xwalk

#endif  // XWALK_EXTENSIONS_RENDERER_XWALK_EXTENSION_CLIENT_H_