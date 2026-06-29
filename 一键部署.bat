@echo off
chcp 65001 >nul
cd /d "C:\Users\ASDCF\.qclaw\workspace"

echo ============================================
echo  一键部署 — 丝路山海通后台局域网访问
echo ============================================
echo.

:: 第1步：开放防火墙
echo [1/3] 开放防火墙 8080 端口...
netsh advfirewall firewall add rule name="丝路山海通后台" dir=in action=allow protocol=TCP localport=8080 >nul 2>&1
echo ✅ 防火墙已开放
echo.

:: 第2步：测试服务是否在运行，不在就启动
echo [2/3] 检查服务状态...
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if %ERRORLEVEL% NEQ 0 (
    start /B python3 admin_server.py
    echo ✅ 后台服务已启动
) else (
    echo ✅ 后台服务已在运行中
)
echo.

:: 第3步：添加到开机启动
echo [3/3] 添加到开机自启...
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set VBS_PATH="%STARTUP_DIR%\丝路山海通后台.vbs"

echo Set WshShell = CreateObject("WScript.Shell") > %TEMP%\start_server.vbs
echo WshShell.Run chr(34) ^& "C:\Users\ASDCF\.qclaw\workspace\start_server.vbs" ^& chr(34), 0, False >> %TEMP%\start_server.vbs

:: 直接用 VBS 实现无窗口启动
echo Set WshShell = CreateObject("WScript.Shell") > %STARTUP_DIR%\丝路山海通后台.vbs
echo WshShell.Run "python3 ""C:\Users\ASDCF\.qclaw\workspace\admin_server.py""", 0, False >> %STARTUP_DIR%\丝路山海通后台.vbs
echo ✅ 已添加到开机自启（无窗口静默启动）
echo.

:: 显示访问信息
echo ============================================
echo  ✅ 部署完成！
echo ============================================
echo.
echo  本地访问:
echo    后台: http://localhost:8080/admin
echo    预览: http://localhost:8080/preview
echo.
echo  同一局域网内其他电脑访问:
echo    后台: http://192.168.110.39:8080/admin
echo    预览: http://192.168.110.39:8080/preview
echo    登录: http://192.168.110.39:8080/login
echo.
echo  ※ 其他电脑需要连接同一个 WiFi/网络
echo  ※ 用户名: jackleework  密码: 999999
echo.
echo ============================================
pause
