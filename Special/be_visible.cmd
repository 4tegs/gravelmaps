@echo off
setlocal enabledelayedexpansion
if "%~1"=="" goto error

:: check the existence of gmaptool
if not exist "%~dps0gmt.exe" goto error

:: check the existence of the chosen file
if not exist "%~1" goto error

echo.

:: change visibility in Basecamp
%~dps0gmt.exe -w -c 0.0,0 "%~1"

echo.
echo.
echo Visibility in Basecamp changed for "%~1"
goto end

:error
echo.
echo.
echo Prerequisite:
echo.
echo Keep the files be_visible.cmd and gmt.exe together in the same folder.
echo.
echo Usage:
echo.
echo Drag the gmapsupp.img file to the icon of be_visible.cmd. 
echo 

:end
echo.
echo.
pause