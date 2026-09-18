<#
  polish-profile.ps1 — sets descriptions, topics and homepages on SSS-R's repos.

  Every description below was written from the repo's ACTUAL contents (README,
  file tree, package.json), not guessed. Edit any line you disagree with before
  running — you know these better than a file listing does.

  Requires: gh CLI, authenticated (gh auth status)
  Dry run : .\polish-profile.ps1
  Apply   : .\polish-profile.ps1 -Apply
#>

param([switch]$Apply)

$repos = @(
  # ---- Flagship: real products ----
  @{ n='pdf-splitter'; d='Browser-only PDF toolkit — split, merge, compress, reorder, images to PDF. Your files never leave your device.';
     h='https://sss-r.github.io/pdf-splitter/'; t=@('pdf','privacy','client-side','vite','javascript','pdf-tools','no-upload','webapp') }

  @{ n='Master-Sentinal'; d='Free, open-source Windows diagnostics hub — live dashboard, guided health scan with real repair tools, shareable reports. No telemetry.';
     h=''; t=@('windows','diagnostics','python','system-monitoring','sysadmin','open-source','desktop-app') }

  @{ n='Zenfa-AI'; d='Hybrid knapsack + LLM engine that optimizes PC builds for the Bangladesh market.';
     h=''; t=@('llm','fastapi','optimization','gemini','python','agentic-ai','recommendation-engine') }

  @{ n='Automations-agent'; d='Auto-Clipper — long YouTube videos into vertical short-form clips, with AI-picked moments. Shelved.';
     h=''; t=@('ai','video-editing','remotion','gemini','python','shorts','automation','content-creation') }

  @{ n='ai-dev-cli'; d='Five-agent pipeline — Planner, Builder, Tester, Fixer, Deployer. Shelved.';
     h=''; t=@('ai-agents','cli','python','llm','multi-agent','developer-tools','automation') }

  @{ n='UPI'; d='Solving the FIFA Paradox — a Unified Performance Index that rates footballers on every deliberate action, built on StatsBomb open data.';
     h=''; t=@('data-science','sports-analytics','football','jupyter','statsbomb','research','python') }

  @{ n='Wrestle-Rumble'; d='Full-stack card game platform — auth, deck economy and database design. Academic project, not maintained.';
     h='https://sss-r.github.io/Wrestle-Rumble'; t=@('nextjs','fastapi','postgresql','typescript','game','fullstack') }

  # ---- Solid supporting work ----
  @{ n='project-zenfa'; d='The full Zenfa platform — B2B and B2C storefronts, backend services and scrapers around the Zenfa AI engine.';
     h=''; t=@('nextjs','typescript','fastapi','monorepo','ecommerce','docker') }

  @{ n='Al-Mursalaat'; d='FastAPI admissions and admin backend — JWT auth, rate limiting, Alembic migrations, email dispatch and Google Sheets sync.';
     h=''; t=@('fastapi','python','jwt','sqlalchemy','rest-api','backend','alembic') }

  @{ n='mobile-agent-pc'; d='WebSocket bridge for driving local AI coding agents from your phone, behind a permissions and command-validation layer.';
     h=''; t=@('websocket','python','ai-agents','remote-control','mobile','developer-tools') }

  @{ n='lyra-mentor-mcp'; d='MCP server experiment in TypeScript.';
     h=''; t=@('mcp','typescript','model-context-protocol','ai') }

  @{ n='Zenfa.AI'; d='Promotional landing page for PC Lagbe? and the Zenfa AI platform.';
     h=''; t=@('landing-page','vite','marketing-site','css') }

  @{ n='Re-vibe'; d='Next.js + Remotion scaffold. Early work in progress.';
     h=''; t=@('nextjs','remotion','wip') }

  # ---- Portfolio iterations ----
  @{ n='Protfolio'; d='Portfolio rebuild — Next.js, spec-driven with a written PRD and agent briefs.';
     h=''; t=@('nextjs','portfolio','typescript','tailwindcss') }

  @{ n='quantum-portfolio'; d='Portfolio concept build — Next.js and Tailwind.';
     h=''; t=@('nextjs','portfolio','typescript','tailwindcss') }

  @{ n='website'; d='Earlier portfolio iteration — Next.js with shadcn/ui.';
     h='REMOVE'; t=@('nextjs','portfolio','shadcn-ui','typescript') }   # homepage 404s — clearing it

  # ---- Coursework (honest labels beat no labels) ----
  @{ n='MetaData-Journaling-CSE-321-'; d='Filesystem metadata journaling in C — CSE321 Operating Systems group project.';
     h=''; t=@('c','operating-systems','filesystem','coursework','bracu') }

  @{ n='DS-Bracu'; d='Data structures coursework — BSTs, graphs, heaps and trees worked through in Jupyter.';
     h=''; t=@('data-structures','jupyter','coursework','bracu','algorithms') }

  @{ n='DS-A'; d='Data structures and algorithms practice in Java.';
     h=''; t=@('java','algorithms','data-structures','practice') }

  @{ n='CSE422'; d='CSE422 lab work — BRAC University.';
     h=''; t=@('python','coursework','bracu') }

  @{ n='Never-been-there'; d='CSE221 lab work plus FastAPI experiments.';
     h=''; t=@('python','fastapi','coursework','bracu') }
)

Write-Host ""
if (-not $Apply) { Write-Host "DRY RUN — nothing will change. Re-run with -Apply to commit." -ForegroundColor Yellow }
Write-Host ""

foreach ($r in $repos) {
  $slug = "SSS-R/$($r.n)"
  $ghArgs = @('repo','edit',$slug,'--description',$r.d)
  foreach ($topic in $r.t) { $ghArgs += @('--add-topic',$topic) }
  # NB: PowerShell drops an empty string when splatting to a native exe, so
  # '--homepage ""' reaches gh as a flag with no argument and the call fails.
  # Clearing a homepage has to go through the API instead.
  $clearHome = ($r.h -eq 'REMOVE')
  if (-not $clearHome -and $r.h) { $ghArgs += @('--homepage',$r.h) }

  if ($Apply) {
    Write-Host "-> $slug" -ForegroundColor Cyan
    & gh @ghArgs
    if ($LASTEXITCODE -ne 0) { Write-Host "   FAILED ($LASTEXITCODE)" -ForegroundColor Red }
    if ($clearHome) {
      '{"homepage":""}' | & gh api --method PATCH "repos/$slug" --input - | Out-Null
    }
  } else {
    Write-Host "-> $slug" -ForegroundColor Cyan
    Write-Host "   $($r.d)" -ForegroundColor Gray
    Write-Host "   topics: $($r.t -join ', ')" -ForegroundColor DarkGray
  }
}

Write-Host ""
Write-Host "NEXT: archive the dead ones. Descriptions are set above first, because" -ForegroundColor Yellow
Write-Host "'gh repo edit' fails once a repo is archived." -ForegroundColor Yellow
Write-Host ""
Write-Host "  # Shelved by your own call - archiving marks them read-only and"
Write-Host "  # shows a 'Public archive' badge, which reads as deliberate."
Write-Host "  gh repo archive SSS-R/Automations-agent"
Write-Host "  gh repo archive SSS-R/ai-dev-cli"
Write-Host ""
Write-Host "  # Wrestle-Rumble uses WWE marks and assets. Archiving leaves it public"
Write-Host "  # and still infringing - make it private instead if that worries you."
Write-Host "  gh repo edit SSS-R/Wrestle-Rumble --visibility private --accept-visibility-change-consequences"
Write-Host ""
Write-Host "  # Early learning repos, diluting the profile."
Write-Host "  gh repo archive SSS-R/python"
Write-Host "  gh repo archive SSS-R/Python-Data-Structures-Michigan"
Write-Host "  gh repo archive SSS-R/Google-git"
Write-Host "  gh repo delete  SSS-R/it-cert-automation-practice   # an unmodified fork"
Write-Host ""
