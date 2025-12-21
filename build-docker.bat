@echo off
REM Build script for ChatPPT Docker images (Windows)

echo ======================================
echo ChatPPT Docker Build Script (Windows)
echo ======================================
echo.

REM Default values
set BUILD_TYPE=cpu
set VERSION=latest
set REGISTRY=
set PUSH=false

REM Parse arguments
:parse_args
if "%1"=="" goto end_parse
if /i "%1"=="-t" (
    set BUILD_TYPE=%2
    shift
    shift
    goto parse_args
)
if /i "%1"=="--type" (
    set BUILD_TYPE=%2
    shift
    shift
    goto parse_args
)
if /i "%1"=="-v" (
    set VERSION=%2
    shift
    shift
    goto parse_args
)
if /i "%1"=="--version" (
    set VERSION=%2
    shift
    shift
    goto parse_args
)
if /i "%1"=="-r" (
    set REGISTRY=%2
    shift
    shift
    goto parse_args
)
if /i "%1"=="--registry" (
    set REGISTRY=%2
    shift
    shift
    goto parse_args
)
if /i "%1"=="-p" (
    set PUSH=true
    shift
    goto parse_args
)
if /i "%1"=="--push" (
    set PUSH=true
    shift
    goto parse_args
)
if /i "%1"=="-h" goto show_help
if /i "%1"=="--help" goto show_help
shift
goto parse_args

:end_parse

REM Set image name
if not "%REGISTRY%"=="" (
    set IMAGE_NAME=%REGISTRY%
) else (
    set IMAGE_NAME=chatppt
)

echo Build Configuration:
echo   Type: %BUILD_TYPE%
echo   Version: %VERSION%
echo   Image: %IMAGE_NAME%
echo   Push: %PUSH%
echo.

REM Build based on type
if /i "%BUILD_TYPE%"=="all" (
    call :build_image cpu
    call :build_image gpu
) else (
    call :build_image %BUILD_TYPE%
)

echo.
echo ======================================
echo Build completed successfully!
echo ======================================
echo.
echo To run the container:
if /i "%BUILD_TYPE%"=="gpu" echo   docker run -p 7860:7860 --gpus all %IMAGE_NAME%:latest-gpu
if /i "%BUILD_TYPE%"=="cpu" echo   docker run -p 7860:7860 %IMAGE_NAME%:latest-cpu
if /i "%BUILD_TYPE%"=="all" (
    echo   docker run -p 7860:7860 %IMAGE_NAME%:latest-cpu
    echo   docker run -p 7860:7860 --gpus all %IMAGE_NAME%:latest-gpu
)
echo.
echo Or use docker-compose:
echo   docker-compose up -d
echo.
pause
exit /b 0

:build_image
set VARIANT=%1
set DOCKERFILE=Dockerfile.%VARIANT%
set TAG=%IMAGE_NAME%:%VERSION%-%VARIANT%

echo.
echo Building %VARIANT% image: %TAG%
echo --------------------------------------

if not exist "%DOCKERFILE%" (
    echo Error: Dockerfile not found: %DOCKERFILE%
    exit /b 1
)

docker build -f "%DOCKERFILE%" -t "%TAG%" .
if errorlevel 1 (
    echo Error building image
    exit /b 1
)

REM Tag as latest
docker tag "%TAG%" "%IMAGE_NAME%:latest-%VARIANT%"

echo Successfully built: %TAG%

REM Push if requested
if /i "%PUSH%"=="true" (
    echo Pushing %TAG% to registry...
    docker push "%TAG%"
    docker push "%IMAGE_NAME%:latest-%VARIANT%"
    echo Successfully pushed: %TAG%
)

exit /b 0

:show_help
echo Usage: build-docker.bat [OPTIONS]
echo.
echo Options:
echo   -t, --type TYPE      Build type: cpu, gpu, or all (default: cpu)
echo   -v, --version VER    Version tag (default: latest)
echo   -r, --registry REG   Registry URL (default: none)
echo   -p, --push           Push to registry after build
echo   -h, --help           Show this help message
echo.
echo Examples:
echo   build-docker.bat --type cpu
echo   build-docker.bat --type all --version 1.0.0
echo   build-docker.bat --type cpu --registry ghcr.io/myuser/chatppt --push
exit /b 0

