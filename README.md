# KU 2020 Degree Candidates Data Extraction

This project extracts degree candidate information (name, major, and school) from a KU 2020 graduation HTML file and saves it into a well-organized Excel spreadsheet.

---

## Features

- Parses the provided HTML file to extract candidate names, majors, and schools.
- Handles multiple schools and degree programs.
- Cleans candidate names by removing extra degree information.
- Saves the extracted data into an Excel file for easy reference.

---

## Requirements

- Python 3.x  
- pandas  
- beautifulsoup4  
- openpyxl (for Excel output)  

Install dependencies via pip:

```bash
pip install pandas beautifulsoup4 openpyxl
