import sys
if sys.version < '3':
    from urllib import urlencode
    from urllib2 import urlopen, Request
    from StringIO import StringIO
else:
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
    from io import BytesIO as StringIO
import flat.settings as settings
import json
import pycurl


def query(request, query, parsejson=True, **extradata):
    data = {'query':query}
    if 'sid' in request.GET:
        data['sid'] = request.session.session_key + '_' + request.GET['sid']
    else:
        data['sid'] = request.session.session_key + '_NOSID'
    for key, value in extradata.items():
        if isinstance(value, bool):
            data[key] = int(value)
        else:
            data[key] = value
    docservereq = Request("http://" + settings.FOLIADOCSERVE_HOST + ":" + str(settings.FOLIADOCSERVE_PORT) + "/query/")
    f = urlopen(docservereq,urlencode(data).encode('utf-8')) #or opener.open()
    if sys.version < '3':
        contents = unicode(f.read(),'utf-8')
    else:
        contents = str(f.read(),'utf-8')
    f.close()
    if contents and contents[0] in ('{','['):
        #assume this is json
        if parsejson:
            return json.loads(contents)
        else:
            return contents
    elif contents:
        return contents
    else:
        if parsejson:
            return None
        else:
            return ""


def get( request, url, parsejson=True):
    docservereq = Request("http://" + settings.FOLIADOCSERVE_HOST + ":" + str(settings.FOLIADOCSERVE_PORT) + "/" + url) #or opener.open()
    if 'sid' in request.GET:
        sid = request.session.session_key + '_' + request.GET['sid']
        docservereq.add_header('x-sessionid', sid)
    else:
        sid = request.session.session_key + '_NOSID'
        docservereq.add_header('x-sessionid', sid)
    f = urlopen(docservereq)
    if sys.version < '3':
        contents = unicode(f.read(),'utf-8')
    else:
        contents = str(f.read(),'utf-8')
    f.close()
    if contents and contents[0] in ('{','['):
        #assume this is json
        if parsejson:
            return json.loads(contents)
        else:
            return contents
    elif contents:
        return contents
    else:
        if parsejson:
            return None
        else:
            return ""

def postjson( request, url, data):
    if isinstance(data, dict) or isinstance(data,list) or isinstance(data, tuple):
        data = json.dumps(data)
        sid = request.session.session_key + '_NOSID'
    else:
        data = json.loads(data)
        data['sid'] = sid = request.session.session_key + '_' + str(data['sid'])
        data = json.dumps(data)
    req = Request("http://" + settings.FOLIADOCSERVE_HOST + ":" + str(settings.FOLIADOCSERVE_PORT) + "/" + url + '/' + sid) #or opener.open()
    req.add_header('x-sessionid', sid)
    req.add_header('Content-Type', 'application/json')
    f = urlopen(req, urlencode(data).encode('utf-8'))
    if sys.version < '3':
        contents = unicode(f.read(),'utf-8')
    else:
        contents = str(f.read(),'utf-8')
    f.close()
    if contents and contents[0] == '{':
        #assume this is json
        return json.loads(contents)
    elif contents:
        return contents
    else:
        return None

def postxml( request, url, data):
    buf = StringIO()
    c = pycurl.Curl()
    url = "http://" + settings.FOLIADOCSERVE_HOST + ":" + str(settings.FOLIADOCSERVE_PORT) + "/" + url
    c.setopt(c.URL, url.encode('utf-8'))
    #c.setopt(c.HTTPPOST, data.encode('utf-8') )
    c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, data.encode('utf-8'))
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    code = c.getinfo(c.HTTP_CODE)
    contents = buf.getvalue()
    c.close()

    #req = Request("http://" + settings.FOLIADOCSERVE_HOST + ":" + str(settings.FOLIADOCSERVE_PORT) + "/" + url)
    #req.add_header('Content-Type', 'application/xml; charset=utf-8')
    #req.add_data(urlencode({'data':data.encode('utf-8')}))
    #f = urlopen(req)
    #contents = f.read()
    #f.close()
    if contents and contents[0] == '{':
        #assume this is json
        return json.loads(contents)
    elif contents:
        return contents
    else:
        return None
