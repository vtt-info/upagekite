# Copyright (C) 2020, The Beanstalks Project ehf. and Bjarni R. Einarsson.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# See the files README.md and COPYING.txt for more details.
#
import upagekite
import upagekite.httpd
import time
try:
  from boot import settings
except:
  settings = {}


print("=2= Stage two (sample) loaded successfully!")


class MyProto(upagekite.uPageKiteDefaults):
  trace = upagekite.uPageKiteDefaults.log
  debug = upagekite.uPageKiteDefaults.log


def handle_http_request(kite, conn, frame):
  conn.reply(frame, (
      'HTTP/1.0 200 OK\n'
      'Content-Type: text/html\n'
      '\n'
      '<h1>Hello world!</h1>\n'
      '<h2>This is %s at %s, you are %s</h2>\n'
      '<h3>Your request:</h3>\n'
      '<pre>%s</pre>\n'
    ) % (
       kite.name,
       time.time(),
       frame.remote_ip,
       str(frame.payload, 'latin-1').replace('<', '&lt;')))


if settings.get('kite_name') and settings.get('kite_secret'):
  httpd = upagekite.httpd.HTTPD(
    settings['kite_name'],
    '/bootstrap/webroot')
  kite = upagekite.Kite(
    settings['kite_name'],
    settings['kite_secret'],
    handler=httpd.handle_http_request)

  print("=2= Launching uPageKite Hello World: http://%s" % kite.name)
  print("=2= Press CTRL+C to abort and drop to REPL")
  print()
  time.sleep(2)

  upk = upagekite.uPageKite([kite], proto=MyProto)
  upk.run()

else:
  print("=2= No PageKite credentials, launching webrepl instead.")
  import webrepl
  webrepl.start()
