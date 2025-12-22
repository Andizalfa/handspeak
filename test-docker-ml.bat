@echo off
REM Build and run Backend ML Docker container locally

echo ========================================
echo Building Backend ML Docker Image
echo ========================================

cd backend_ml
docker build -t handspeak-ml .

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
echo Starting container on port 8002...
echo.

docker run -p 8002:8002 ^
  -e HF_REPO_ID=Andizalfa05/handspeak ^
  -e PORT=8002 ^
  --name handspeak-ml-test ^
  handspeak-ml

echo.
echo Container stopped.
echo.
echo To remove container: docker rm handspeak-ml-test
pause
