with open('index.html', encoding='utf-8') as f:
    html = f.read()

OLD = "  } catch(e) {\n    document.getElementById('loading').innerHTML =\n      '<p style=\"color:#e8001c\">\u26a0 Could not load data/vip_data.json<br><small style=\"color:#94a3b8\">Serve this page from a web server (not file://)</small></p>';\n    console.error(e);\n  }"

NEW = "  } catch(e) {\n    document.getElementById('loading').innerHTML =\n      '<p style=\"color:#e8001c\">\u26a0 ' + e.name + ': ' + e.message +\n      '<br><small style=\"color:#94a3b8\">Open browser console (F12) for full trace</small></p>';\n    console.error('DASHBOARD INIT FAILED:', e.name, e.message, e.stack);\n  }"

if OLD in html:
    html = html.replace(OLD, NEW)
    print("Updated catch block")
else:
    print("NOT FOUND - showing surrounding context:")
    idx = html.find("Could not load")
    print(repr(html[idx-100:idx+200]))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
