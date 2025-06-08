import pandas as pd
from bs4 import BeautifulSoup
import re

def extract_candidates_from_html(html_file_path):
    """
    Extracts names and majors of degree candidates from an HTML file.

    Args:
        html_file_path (str): The path to the HTML file containing the candidate data.

    Returns:
        list: A list of dictionaries, where each dictionary contains 'Name' and 'Major'.
    """
    candidates_data = []

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: HTML file not found at '{html_file_path}'")
        return []
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all school sections
    school_sections = soup.find_all('div', class_='school')

    if not school_sections:
        print("No school sections found. Please check HTML structure (div class='school').")
        return []

    for school_section in school_sections:
        # Extract the school name (e.g., School of Architecture & Design)
        school_name_tag = school_section.find('h2', class_='school__name')
        school_name = school_name_tag.get_text(strip=True) if school_name_tag else "Unknown School"
        
        # Find all degree sections within the current school
        degree_sections = school_section.find_all('div', class_='degree_wrapper')

        if not degree_sections:
            print(f"No degree programs found for {school_name}. Please check HTML structure (div class='degree_wrapper').")
            continue

        for degree_section in degree_sections:
            # Extract the major/program name (e.g., Architecture, Design)
            major_name_tag = degree_section.find('h4', class_='degree__h4')
            major_name = major_name_tag.get_text(strip=True) if major_name_tag else "Unknown Major"

            # Find the list of candidates for this major
            candidate_list = degree_section.find('ul', class_='list-unstyled')
            
            if candidate_list:
                # Extract each candidate's name
                for li in candidate_list.find_all('li'):
                    name = li.get_text(strip=True)
                    # Clean up the name (remove degree info if present)
                    name = re.sub(r',\s*[A-Za-z\s]*$', '', name).strip()
                    
                    candidates_data.append({
                        'Name': name,
                        'Major': major_name,
                        'School': school_name
                    })
            else:
                print(f"No candidate list found for {school_name} - {major_name}.")

    return candidates_data

def save_to_excel(data, output_excel_path, sheet_name='Candidates'):
    """
    Saves a list of dictionaries to an Excel file.

    Args:
        data (list): A list of dictionaries to save.
        output_excel_path (str): The path where the Excel file will be saved.
        sheet_name (str): The name of the sheet in the Excel file.
    """
    if not data:
        print("No data to save to Excel.")
        return

    try:
        df = pd.DataFrame(data)
        # Ensure column order
        df = df[['Name', 'Major', 'School']]
        df.to_excel(output_excel_path, index=False, sheet_name=sheet_name)
        print(f"Data successfully saved to '{output_excel_path}' on sheet '{sheet_name}'.")
    except Exception as e:
        print(f"Error saving data to Excel: {e}")

# --- Main execution ---
if __name__ == "__main__":
    # Define the path to your HTML file
    html_file = 'ku_graduation_commencement_2020.html'

    # Define the desired output Excel file name
    output_file = 'KU_2020_Degree_Candidates.xlsx'

    print(f"Starting data extraction from '{html_file}'...")
    extracted_data = extract_candidates_from_html(html_file)

    if extracted_data:
        print(f"Extracted {len(extracted_data)} candidate entries.")
        print(f"Saving extracted data to '{output_file}'...")
        save_to_excel(extracted_data, output_file)
    else:
        print("No data was extracted. The Excel file will not be created.")