@echo off
call C:\Users\erick\anaconda3\Scripts\activate.bat
cd "C:\Users\erick\OneDrive\Desktop\Python\econ_dashboard"
echo Starting Streamlit app...
streamlit run econ_dashboard.py

echo.
echo 💡 Press any key to exit.
pause >nul

