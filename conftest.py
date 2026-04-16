"""
Root conftest.py — auto-install ChromeDriver so Dash browser tests work.
"""
import os
from webdriver_manager.chrome import ChromeDriverManager

# Download ChromeDriver if it's not already available on PATH
os.environ["PATH"] += os.pathsep + os.path.dirname(
    ChromeDriverManager().install()
)
