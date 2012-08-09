import mimetypes, os, zipfile
from flask import Flask, redirect, safe_join, url_for, Response
app = Flask(__name__)

repo = os.path.expanduser('~/.m2/repository')

@app.route('/class/<deplist>/<classname>')
def findclass(deplist, classname):
    deps = [dep.split(':') for dep in deplist.split(',')]
    paths = ['%s/%s/%s/%s-%s-javadoc.jar' % (d[0].replace('.', '/'), d[1], d[2], d[1], d[2]) for d in deps]
    classdocpath = classname.replace('.', '/') + ".html"
    for path in paths:
        fullpath = safe_join(repo, path)
        if not os.path.exists(fullpath):
            continue
        jar = zipfile.ZipFile(fullpath, 'r')
        if classdocpath in jar.namelist():
            return redirect(url_for('fromrepo', location='%s/%s' % (path, classdocpath)))
    return "Not found"

@app.route('/repo/<path:location>')
def fromrepo(location):
    jarindex = location.index('.jar/')
    injar = location[jarindex + 5:]
    jar = zipfile.ZipFile(safe_join(repo, location[:jarindex + 4]), 'r')
    return Response(jar.open(injar), mimetype=mimetypes.guess_type(injar)[0])

if __name__ == '__main__':
    app.run(debug=True)