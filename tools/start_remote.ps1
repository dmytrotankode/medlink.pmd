# Запуск ЛОКАЛЬНОЇ сесії Claude Code з керуванням з телефону (Remote Control).
# Сесія виконується на цьому комп'ютері, у застосунку Claude (вкладка Code) з'являється як "MEDLINK".
#   .\tools\start_remote.ps1            — інтерактивна сесія в терміналі + доступ з телефону
#   .\tools\start_remote.ps1 -Server    — лише сервер Remote Control (без локального чату), QR-код по пробілу
#   .\tools\start_remote.ps1 -Continue  — повернути попередню сесію MEDLINK цієї папки
param([switch]$Server, [switch]$Continue, [string]$Name = "PMG")

Set-Location (Split-Path $PSScriptRoot -Parent)
$env:CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX = "MEDLINK"

if ($Server) {
    if ($Continue) { claude remote-control --name $Name --continue } else { claude remote-control --name $Name }
} elseif ($Continue) {
    claude --resume $Name
} else {
    claude --remote-control $Name
}
