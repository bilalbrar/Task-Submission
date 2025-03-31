import os
import sys
import argparse
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.core.logging import logger

# Download NLTK data
nltk.download('punkt', quiet=True)

# Rest of the code remains the same... 