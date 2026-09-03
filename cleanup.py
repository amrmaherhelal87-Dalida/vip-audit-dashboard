with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Restore clean error message in catch block
OLD = "  } catch(e) {\n    document.getElementById('loading').innerHTML =\n      '<p style=\"color:#e8001c\">\u26a0 ' + e.name + ': ' + e.message +\n      '<br><small style=\"color:#94a3b8\">Open browser console (F12) for full trace</small></p>';\n    console.error('DASHBOARD INIT FAILED:', e.name, e.message, e.stack);\n  }"

NEW = "  } catch(e) {\n    document.getElementById('loading').innerHTML =\n      '<p style=\"color:#e8001c\">\u26a0 Dashboard failed to load<br>' +\n      '<small style=\"color:#94a3b8\">' + e.name + ': ' + e.message + '</small></p>';\n    console.error('DASHBOARD INIT FAILED:', e);\n  }"

if OLD in html:
    html = html.replace(OLD, NEW)
    print("Catch block cleaned up")
else:
    print("Not found - no change needed")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
