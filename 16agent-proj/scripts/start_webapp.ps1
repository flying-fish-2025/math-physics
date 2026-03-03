param(
    [int]$Port = 8501
)

Write-Host "Cleaning old Streamlit processes on port $Port ..."

$conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
foreach ($conn in $conns) {
    try {
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    } catch {
    }
}

$streamlitLike = Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match "streamlit run src/math_agent_mcp/webapp.py" }
foreach ($p in $streamlitLike) {
    try {
        Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    } catch {
    }
}

Write-Host "Starting Streamlit on fixed port $Port ..."
micromamba run -n math-agent-win streamlit run src/math_agent_mcp/webapp.py --server.port $Port

