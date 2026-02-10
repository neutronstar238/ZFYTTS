@echo off
chcp 65001 >nul
echo ========================================
echo   卸载定时清理任务
echo ========================================
echo.
echo 此脚本将删除自动清理的定时任务
echo.
pause

set TASK_NAME=GPT-SoVITS-Cleanup

echo.
echo 正在删除定时任务: %TASK_NAME%
echo.

schtasks /Delete /TN "%TASK_NAME%" /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ 定时任务已成功删除！
    echo.
) else (
    echo.
    echo ✗ 任务删除失败或任务不存在
    echo.
)

pause
