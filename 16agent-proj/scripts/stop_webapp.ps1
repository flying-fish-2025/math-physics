param(
    [int]$Port = 8501
)

Write-Host "Stopping Streamlit webapp processes..."

$patterns = @(
    "streamlit run src/math_agent_mcp/webapp.py",
    "micromamba run -n math-agent-win streamlit run src/math_agent_mcp/webapp.py"
)

$filtered = @()
foreach ($p in (Get-CimInstance Win32_Process)) {
    if ($p.Name -notin @("python.exe", "micromamba.exe", "streamlit.exe")) {
        continue
    }
    if (-not $p.CommandLine) {
        continue
    }
    foreach ($pat in $patterns) {
        if ($p.CommandLine -like "*$pat*") {
            $filtered += $p
            break
        }
    }
}

$procIds = $filtered | Select-Object -ExpandProperty ProcessId -Unique
foreach ($procId in $procIds) {
    try {
        taskkill /PID $procId /T /F | Out-Null
        Write-Host "Stopped process tree PID $procId"
    } catch {
    }
}

# Extra safety: if the specified port is still occupied, kill its owner.
$conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($conn) {
    foreach ($c in $conn) {
        try {
            taskkill /PID $c.OwningProcess /T /F | Out-Null
            Write-Host "Stopped port owner PID $($c.OwningProcess) on $Port"
        } catch {
        }
    }
}

