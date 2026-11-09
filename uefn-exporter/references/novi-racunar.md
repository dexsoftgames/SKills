# Instructions for the agent: set up a new computer exactly like Dejan's

You are an agent (Claude Code) on a new computer. Your job is to set up everything below so that this computer works
**exactly like Dejan's main machine**: Claude Code can connect at any time to an open Unreal Engine 5.8 project
and to UEFN (Unreal Editor for Fortnite) through MCP, and the **Export To UEFN** plugin works.

Written on 29 Sep 2026 on the main machine. Dejan has the same versions of all programs on both computers.

## General rules

- Work in the order of the steps. After each step, run its **check**. Don't move on until the check passes.
- Paths below are the ones on the main machine (`H:\`, `J:\`, `C:\Users\dejan`). If a drive or user name is different
  on the new computer, use the correct path everywhere, and write down at the end what you changed.
- **Never** run UE 5.8 and UEFN at the same time (it crashes the GPU). Check `tasklist` before starting either.
- Don't touch git history. Commits happen only when Dejan says "submituj git".

---

## 1. Base programs (same versions)

| Program | Version on the main machine | Where to get it |
|---|---|---|
| Unreal Engine | **5.8.1** (CL 56057345) | Epic Games Launcher → Unreal Engine → Library → 5.8. On the main machine it is installed at `J:\EpicGamesDownloadFiles\UE_5.8` (**not** in Program Files, and not in the registry) |
| Fortnite + UEFN | Fortnite **42.20** / UEFN 6.0 | Epic Games Launcher → Fortnite, then Unreal Editor for Fortnite. Executable: `C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\UnrealEditorFortnite-Win64-Shipping.exe` |
| Visual Studio | **VS 2026 Community 18.8**, MSVC **14.51.36231**, Windows SDK **10.0.22621.0** | visualstudio.microsoft.com. Workloads: "Game development with C++" and "Desktop development with C++"; under Individual components, check MSVC 14.51 and Windows 11 SDK 10.0.22621 |
| Node.js | **v24.16.0** | nodejs.org, Windows installer (x64). Must be at `C:\Program Files\nodejs\` |
| Python | **3.14.5** | python.org, Windows installer. Check **"Add python.exe to PATH"** |
| uv | **0.11.19** | PowerShell: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` → ends up in `C:\Users\<user>\.local\bin\uv.exe` |
| Git | any recent version | git-scm.com |
| Claude Code | latest | `npm install -g @anthropic-ai/claude-code`, plus the Claude Code extension for VS Code |

**Check:**
```powershell
& "C:\Program Files\nodejs\node.exe" --version      # v24.16.0
python --version                                      # Python 3.14.5
& "$env:USERPROFILE\.local\bin\uv.exe" --version      # uv 0.11.19
Test-Path "J:\EpicGamesDownloadFiles\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
Test-Path "C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\UnrealEditorFortnite-Win64-Shipping.exe"
```

### 1a. Force the VS 2026 toolchain (otherwise UE picks VS 2022 without any error)

Create `%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml`:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
	<WindowsPlatform>
		<Compiler>VisualStudio2026</Compiler>
		<CompilerVersion>14.51.36231</CompilerVersion>
		<ToolchainVersion>14.51.36231</ToolchainVersion>
	</WindowsPlatform>
</Configuration>
```

`<Compiler>` on its own is **not** enough; the version pins are what make it work. After **every** change to this file,
delete both caches:
- `<project>\Intermediate\Build\XmlConfigCache.bin`
- `%LOCALAPPDATA%\UnrealEngine\XmlConfigCache-J+EpicGamesDownloadFiles+UE_5.8.bin` (the name follows the engine path)

**Check:** after a build, `%LOCALAPPDATA%\UnrealBuildTool\Log.txt` contains `Using Visual Studio 14.51...`.

---

## 2. Project folders

Copy these folders from the main machine (or from the backup) with the **same paths**:

- `H:\UnrealToUEFN\` — the whole folder: `Plugin\`, `PluginBuild\`, `UnrealProjects\`, `UEFN\`, `Docs\`, `BuildPlugin.ps1`,
  `CLAUDE.md`, `UEFNExporterTest.md`, `.mcp.json`
- `H:\MaloSeoce2\MaloSeoce_5.8\` — the game project (only if this computer works on the game too)

Read `H:\UnrealToUEFN\CLAUDE.md` first. It holds all the working rules and the main rules (project name = the folder in
Content, the map in `Maps`, the Blank template, sounds, glass...).

---

## 3. MCP servers — the connection between Claude Code and the editors

There are **three** MCP connections to Unreal/UEFN. All three have to work.

### 3a. `ue-mcp` — the main bridge to UE 5.8 (1900+ actions)

- npm package **`ue-mcp` version 1.3.9**. It starts through `npx`, so there is nothing to install by hand.
- On its first connection to a project, it installs the **UE_MCP_Bridge** C++ plugin into that project's `Plugins\UE_MCP_Bridge\`
  and enables it in the `.uproject` (`"UE_MCP_Bridge": true`). The editor then has to be restarted once so the plugin
  compiles and loads.
- Each project must have in its `.uproject`: `PythonScriptPlugin=true` (ue-mcp uses Python for some actions).
- **Why the other computer keeps asking for something to be enabled:** ue-mcp copies only the SOURCE of the bridge
  (`Plugins\UE_MCP_Bridge\Source`) into a project, never compiled binaries. On the first open of that project, Unreal says
  "missing modules, rebuild?" and compiles it with Visual Studio. If VS 2026 / MSVC 14.51 and `BuildConfiguration.xml`
  (step 1a) are not set up properly, the compile fails and it asks again every time. On the main machine this
  was done once per project, so there is no prompt any more.
  Doing it right, once per project:
  1. `npx -y ue-mcp init "<path>\<Project>.uproject"`: deploys the bridge and enables UE_MCP_Bridge + PythonScriptPlugin.
  2. Open the project in UE 5.8 once and answer **Yes** to "rebuild". Wait for it to finish, then close.
     From then on it opens without questions, and ue-mcp connects by itself.
  3. If it doesn't connect: `npx -y ue-mcp doctor`, and in the Output Log look for `UE_MCP_Bridge` (compile error).
  Every new project the agent opens with `set_project` goes through the same thing once.
- The bridge finds the editor's port by itself through a lockfile. `project(action="set_project", projectPath=...)` switches
  the bridge to any other open project, so **you can connect to whichever project is open at any time**.

### 3b. `unreal-epic` — Epic's built-in MCP in UE 5.8 (port 8000)

- Engine plugin: `Engine\Plugins\Experimental\ModelContextProtocol` (it ships with UE 5.8).
- In the project: Edit → Plugins → search "Model Context Protocol" → Enable, then restart the editor.
- Editor Preferences → Model Context Protocol → **Server Port Number = 8000**, turn on **Auto Start Server**.
- Endpoint: `http://127.0.0.1:8000/mcp`

### 3c. `uefn` — UEFN's built-in MCP (port 8001)

For **each** UEFN project (once, by hand):
1. UEFN → Project Settings → **Experimental Access**: turn on **Python Editor Scripting**.
2. Project Settings → **Beta Access**: turn on **UEFN MCP Toolsets**.
3. Editor Preferences → **Server Port Number = 8001**. Not 8000, because UE 5.8 already listens there and the two would collide.
4. Restart UEFN. The server only starts and stops on a restart.

Where UEFN stores this (so you can check it or set it with the editor **closed**):
- Port: `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Config\WindowsEditor\EditorPerProjectUserSettings.ini` →
  `ServerPortNumber=8001`
- Python per project: in the same ini, `EnablePythonLocallyPerProject=((<projectId>, True))`
- Toolsets per project: in `<Project>.uefnproject` → `dataSets.experimental.toolsets.bEnableToolsetsForProject: true`
  (the **Export To UEFN** exporter writes this by itself on export)
- A config can only be changed while UEFN is closed, because UEFN overwrites it on exit.

Endpoint: `http://127.0.0.1:8001/mcp`. Meta-tools: `list_toolsets`, `describe_toolset`, `call_tool`
(with `toolset_name`, `tool_name`, `arguments`).

### 3d. The `.mcp.json` file

`H:\UnrealToUEFN\.mcp.json` (Claude Code is launched from `H:\UnrealToUEFN`):

```json
{
  "mcpServers": {
    "ue-mcp": {
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": ["-y", "ue-mcp", "H:/UnrealToUEFN/UnrealProjects/CoffeeHouseTest/CoffeeHouseTest.uproject"]
    },
    "unreal-epic": { "type": "http", "url": "http://127.0.0.1:8000/mcp" },
    "uefn":        { "type": "http", "url": "http://127.0.0.1:8001/mcp" }
  }
}
```

The `.uproject` path in `ue-mcp` is only the starting project. Switch to another one at runtime with `set_project`.

`H:\MaloSeoce2\MaloSeoce_5.8\.mcp.json` (only for work on the game) additionally has `unity` (http 8080), `photoshop`
(`npx -y @alisaitteke/photoshop-mcp`), and two older Unreal bridges (`unreal-voodoofox`, `unreal-chongdashu` through `uv`
from `D:\MCP\...`). Those two are no longer used and need not be set up.

Global (`C:\Users\<user>\.claude.json` → `mcpServers`), optional:
- `photoshop`: `npx -y @alisaitteke/photoshop-mcp`
- `plantfactory`: `uv run --script H:\PlantFactoryMCP\plantfactory_mcp.py`

### 3e. Checking all three MCPs

1. Start UE 5.8 with a test project (use UE_MCP_Bridge + ModelContextProtocol):
   ```powershell
   & "J:\EpicGamesDownloadFiles\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" "H:\UnrealToUEFN\UnrealProjects\Test10\Test10.uproject" -ini:Engine:[/Script/Engine.RendererSettings]:r.Shadow.Virtual.Enable=0 -ini:Engine:[SystemSettings]:r.Shadow.Virtual.Enable=0
   ```
   Wait for the line `Total Editor Startup Time` in `<project>\Saved\Logs\<Project>.log`.
2. In Claude Code: `mcp__ue-mcp__project(action="get_status")` should give `editorConnected: true`.
3. `curl http://127.0.0.1:8000/mcp` should answer (not "connection refused").
4. Close UE, open UEFN with a project, then:
   ```powershell
   python H:\UnrealToUEFN\Docs\uefn_mcp.py call list_toolsets '{}'
   ```
   It should list the toolsets (DeviceToolset, VerseToolset, SessionToolset, SceneTools...). If `SceneTools` /
   `ObjectTools` are missing, Python isn't enabled for the project (step 3c.1).

---

## 4. The Export To UEFN plugin (our exporter)

- Source: `H:\UnrealToUEFN\Plugin\UnrealToUEFN\` (the only place code is changed).
- It depends on engine plugins: Niagara, PythonScriptPlugin, CascadeToNiagaraConverter (all ship with UE 5.8).
- The build goes **only** through `H:\UnrealToUEFN\BuildPlugin.ps1`. It builds into `H:\UnrealToUEFN\PluginBuild\UnrealToUEFN`
  and puts back `"EnabledByDefault": true`. If the engine isn't on `J:`, change `$Engine` at the top of the script.
  **Before the build, close every UE 5.8 editor** (the DLL is locked). UEFN may stay open.
- The engine has to see the plugin through a **junction** (run once, as admin):
  ```cmd
  mklink /J "J:\EpicGamesDownloadFiles\UE_5.8\Engine\Plugins\Marketplace\UnrealToUEFN" "H:\UnrealToUEFN\PluginBuild\UnrealToUEFN"
  ```
  After that, the **Export To UEFN** button shows up in every UE 5.8 project (plus "Simple Collision Maker" when you right-click a mesh).
- `PluginBuild\UnrealToUEFN\Resources\PlaceSounds.py` is the helper that places sounds in UEFN through the MCP.
  It runs on the engine's own Python (`Engine\Binaries\ThirdParty\Python3\Win64\python.exe`), so it needs nothing extra.

**Check:**
```powershell
& H:\UnrealToUEFN\BuildPlugin.ps1     # ends with "BUILD SUCCESSFUL" and "Gotovo: plugin spakovan..."
(Get-Item "J:\EpicGamesDownloadFiles\UE_5.8\Engine\Plugins\Marketplace\UnrealToUEFN").LinkType   # Junction
```
Then in UE: `mcp__ue-mcp__editor(action="execute_command", command="ExportToUEFN H:/UnrealToUEFN/UEFN/<Project>")`.

---

## 5. Claude Code settings

### 5a. Hook against losing unsaved work

Copy `H:\UnrealToUEFN\Docs\block-unsafe-editor-close.py` to `C:\Users\<user>\.claude\hooks\`.
In `C:\Users\<user>\.claude\settings.json`, add:

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "mcp__ue-mcp__editor",
      "hooks": [
        {
          "type": "command",
          "command": "python \"C:/Users/<user>/.claude/hooks/block-unsafe-editor-close.py\"",
          "timeout": 10,
          "statusMessage": "Provera da editor ne gubi nesnimljeno..."
        }
      ]
    }
  ]
}
```

The hook refuses `stop_editor` / `request_editor_shutdown` / `restart_editor` with `requireClean=false` (which throws away
everything unsaved). The correct order is always: `editor(save_dirty)` first, then close.

### 5b. Other settings in `settings.json` (same as the main machine)

```json
"model": "opus",
"modelSettings": { "claude-opus-5-5": { "effortLevel": "high" } },
"autoUpdatesChannel": "latest",
"remoteControlAtStartup": true,
"agentPushNotifEnabled": true,
"permissions": {
  "allow": [ "Bash", "PowerShell", "WebSearch",
             "mcp__ue-mcp__project", "mcp__ue-mcp__editor", "mcp__ue-mcp__asset", "mcp__ue-mcp__level",
             "mcp__ue-mcp__material", "mcp__ue-mcp__blueprint", "mcp__ue-mcp__niagara", "mcp__ue-mcp__audio",
             "mcp__ue-mcp__widget", "mcp__ue-mcp__animation", "mcp__ue-mcp__gameplay", "mcp__ue-mcp__reflection",
             "mcp__plantfactory__*" ],
  "additionalDirectories": [ "C:\\Users\\<user>\\AppData\\Local\\Temp" ]
}
```

### 5c. Memory (what the agent learned on the main machine)

Copy the whole folder
`C:\Users\dejan\.claude\projects\h--MaloSeoce2-MaloSeoce-5-8\memory\`
to the same place on the new computer. The folder name is the project path, so if Claude is launched from
`H:\UnrealToUEFN`, also copy it to `C:\Users\<user>\.claude\projects\H--UnrealToUEFN\memory\`.
`MEMORY.md` is the index; each file is one rule or fact.

---

## 6. Helper scripts (`H:\UnrealToUEFN\Docs\`)

| Script | What it does |
|---|---|
| `uefn_mcp.py` | Small UEFN MCP client: `python uefn_mcp.py list` / `schema <tool>` / `call <tool> '<json>'` |
| `screen.ps1` | Screenshot at half size (click coordinates are ×2), with an optional click: `-ClickX -ClickY [-Double]` |
| `uefn_session.ps1` | Watches a Launch Session and clicks "Make Private" by itself as soon as it appears |
| `close_window.ps1` | Closes a stuck dialog window by title |
| `block-unsafe-editor-close.py` | The hook from step 5a |

Copy them to the session scratchpad when needed, or run them straight from `Docs`.

---

## 7. Final checklist (all must be YES)

- [ ] `node`, `python`, `uv`, UE 5.8, UEFN, and VS 2026 with MSVC 14.51 are in place, same versions (step 1)
- [ ] `BuildConfiguration.xml` is written and the caches deleted (1a)
- [ ] `H:\UnrealToUEFN` is copied, and `CLAUDE.md` is read (2)
- [ ] `ue-mcp` → `get_status` = connected with UE 5.8 open (3a, 3e)
- [ ] `http://127.0.0.1:8000/mcp` answers with UE 5.8 open (3b)
- [ ] `uefn_mcp.py call list_toolsets` lists SceneTools/ObjectTools/DeviceToolset with UEFN open (3c, 3e)
- [ ] `BuildPlugin.ps1` = BUILD SUCCESSFUL, and the junction exists (4)
- [ ] The Export To UEFN button is visible in UE 5.8 (4)
- [ ] Hook, settings.json, and memory are copied (5)

When everything is YES, tell Dejan in one short message: "Sve je postavljeno, isto kao na glavnom racunaru",
and list anything that differs (other drive letters or paths).
