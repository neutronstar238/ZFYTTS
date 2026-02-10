@echo off
chcp 65001 >nul
echo ========================================
echo   安装定时清理任务
echo ========================================
echo.
echo 此脚本将创建一个 Windows 定时任务
echo 每天自动清理 outputs 目录下的旧文件
echo.
echo 需要管理员权限！
echo.
pause

set TASK_NAME=GPT-SoVITS-Cleanup
set SCRIPT_PATH=%~dp0cleanup_outputs.py
set PYTHON_PATH=%~dp0.venv\Scripts\python.exe

echo.
echo 正在创建定时任务...
echo 任务名称: %TASK_NAME%
echo Python 路径: %PYTHON_PATH%
echo 脚本路径: %SCRIPT_PATH%
echo.

REM 删除已存在的任务（如果有）
schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1

REM 创建新任务：每天凌晨 3 点执行一次清理
schtasks /Create /TN "%TASK_NAME%" /TR "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\" --once" /SC DAILY /ST 03:00 /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ 定时任务创建成功！
    echo.
    echo 任务详情：
    echo - 任务名称: %TASK_NAME%
    echo - 执行时间: 每天凌晨 3:00
    echo - 执行操作: 清理超过 1 天的文件
    echo.
    echo 你可以在"任务计划程序"中查看和管理此任务
    echo.
) else (
    echo.
    echo ✗ 任务创建失败！
    echo 请确保以管理员身份运行此脚本
    echo.
)

pause
