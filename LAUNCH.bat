@echo off
set PIDFILE=main.pid

if exist %PIDFILE% (
    taskkill /F /PID %<%PIDFILE% && del %PIDFILE%
)

start /B python main.py >NUL
echo %!errorlevel%! > %PIDFILE%