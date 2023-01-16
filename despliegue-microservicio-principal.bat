@echo off

:: Despliega microservicio principal
python -m uvicorn main:app --reload

