#!/usr/bin/env python3
"""Install the shipped Omarchy Ghostty configuration, with a backup."""
import subprocess

subprocess.run(['omarchy', 'refresh', 'config', 'ghostty/config'], check=True)
subprocess.run(['ghostty', '+validate-config'], check=True)
