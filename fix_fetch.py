with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Add resp.ok check so HTTP errors are caught clearly
OLD_FETCH = "    const resp = await fetch('data/vip_data.json');\n    ALL_DATA = await resp.json();"
NEW_FETCH = "    const resp = await fetch('data/vip_data.json');\n    if (!resp.ok) throw new Error('HTTP ' + resp.status + ' loading vip_data.json');\n    ALL_DATA = await resp.json();"

if OLD_FETCH in html:
    html = html.replace(OLD_FETCH, NEW_FETCH)
    print("Added resp.ok check")
else:
    print("resp.ok: target not found")

# 2. Make catch show REAL error (not generic message)
OLD_CATCH = "  } catch(e) {\n    document.getElementById('loading').innerHTML =\n      '<p style=\"color:#e8001c\">\u26a0 ' + e.name + ': ' + e.message +\n      '<br><small style=\"color:#94a3b8\">Open browser console (F12) for full trace</small></p>';\n    console.error('DASHBOARD INIT FAILED:', e.name, e.message, e.stack);\n  }"

# Check if fix_catch was already applied
if "DASHBOARD INIT FAILED" in html:
    print("catch block already updated with real error")
else:
    # Apply the fix_catch update
    OLD_CATCH2 = "  } catch(e) {\n    document.getElementById('loading').innerHTML =\n      '<p style=\"color:#e8001c\">\u26a0 Could not load data/vip_data.json<br><small style=\"color:#94a3b8\">Serve this page from a web server (not file://)</small></p>';\n    console.error(e);\n  }"
    NEW_CATCH2 = "  } catch(e) {\n    document.getElementById('loading').innerHTML =\n      '<p style=\"color:#e8001c\">\u26a0 ' + e.name + ': ' + e.message +\n      '<br><small style=\"color:#94a3b8\">Open browser console (F12) for full trace</small></p>';\n    console.error('DASHBOARD INIT FAILED:', e.name, e.message, e.stack);\n  }"
    if OLD_CATCH2 in html:
        html = html.replace(OLD_CATCH2, NEW_CATCH2)
        print("Updated catch block")
    else:
        print("catch block: original not found either - checking...")
        idx = html.find("} catch(e)")
        print(repr(html[idx:idx+300]))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done.")
