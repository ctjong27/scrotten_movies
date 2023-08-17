@echo off
setlocal enabledelayedexpansion

REM Check if diagnostic flag is present
if "%~1"=="-d" (
    echo Running diagnostic script...
    python ./scripts/diagnostic_script.py
) else if "%~1"=="-e" (
    echo Running final data cleanup and export
    python ./scripts/tv_data_prep_and_export.py
) else (
    echo Running scripts...
    python ./scripts/tv_show_scraper.py
    python ./scripts/tv_show_season_to_cast_scraper.py
    python ./scripts/tv_cast_scraper.py
    python ./scripts/tv_cast_image_miner.py
    python ./scripts/tv_cast_gender_processor.py
    python ./scripts/tv_season_to_race_gender_count.py
)
pause