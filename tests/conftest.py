import os
import sys
from pathlib import Path

# adiciona a raiz do projeto ao sys.path para que 'backend' seja importável
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
