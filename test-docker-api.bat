@echo off
REM Build and run Backend App Docker container locally

echo ========================================
echo Building Backend App Docker Image
echo ========================================

cd backend
docker build -t handspeak-api .

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Docker build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Docker Image Built Successfully!
echo ========================================
echo.
echo [WARNING] Make sure to set your database credentials!
echo.
echo Starting container on port 8001...
echo.

REM Ganti dengan database credentials Anda
docker run -p 8001:8001 ^
  -e DB_HOST=localhost ^
  -e DB_PORT=3306 ^
  -e DB_USER=root ^
  -e DB_PASSWORD=your-password ^
  -e DB_NAME=bisindo_db ^
  -e ML_SERVICE_URL=http://host.docker.internal:8002 ^
  -e SECRET_KEY=test-secret-key ^
  -e SMTP_HOST=smtp.gmail.com ^
  -e SMTP_PORT=587 ^
  -e SMTP_USER=your-email@gmail.com ^
  -e SMTP_PASSWORD=your-app-password ^
  --name handspeak-api-test ^
  handspeak-api

echo.
echo Container stopped.
echo.
echo To remove container: docker rm handspeak-api-test
pause
