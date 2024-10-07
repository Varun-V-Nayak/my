def extract_multiple_sections(content, start_marker):
    """
    Extracts all occurrences of sections starting from 'start_marker' and ending at a line with only '1'.
    """
    lines = content.splitlines()
    capturing = False
    extracted_sections = []
    current_section = []

    for line in lines:
        if start_marker in line:
            # If we were already capturing a section, store it before starting a new one
            if current_section:
                extracted_sections.append("\n".join(current_section).strip())
                current_section = []

            capturing = True
        
        if capturing:
            current_section.append(line)
        
        if capturing and line.strip() == "1":  # Assumes the section ends at a line containing only "1"
            extracted_sections.append("\n".join(current_section).strip())
            current_section = []
            capturing = False

    return extracted_sections


def highlight_differences(text1, text2):
    """
    Highlight differences between two strings:
    - Strings from file 1 are highlighted in green with a bold and underline style.
    - Strings from file 2 are highlighted in red with a bold and underline style.
    This comparison is done on the basis of words separated by spaces.
    """
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    highlighted_text1 = []
    highlighted_text2 = []

    # Compare line by line
    for line1, line2 in zip(lines1, lines2):
        words1 = line1.split()
        words2 = line2.split()

        # Determine the maximum number of words to compare
        max_words = max(len(words1), len(words2))

        # Compare words
        highlighted_line1 = []
        highlighted_line2 = []

        for i in range(max_words):
            word1 = words1[i] if i < len(words1) else ""
            word2 = words2[i] if i < len(words2) else ""

            if word1 != word2:
                # Highlight differences
                highlighted_line1.append(f"<span class='highlight highlight-file1'>{word1}</span>")
                highlighted_line2.append(f"<span class='highlight highlight-file2'>{word2}</span>")
            else:
                highlighted_line1.append(word1)
                highlighted_line2.append(word2)

        highlighted_text1.append(" ".join(highlighted_line1))
        highlighted_text2.append(" ".join(highlighted_line2))

    return "\n".join(highlighted_text1), "\n".join(highlighted_text2)


def generate_html_report(sections, output_file_path):
    """
    Generates an HTML report comparing sections from two files with enhanced styling.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MV Cells Comparison Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif; 
                background-color: #f4f4f9; 
                color: #333; 
                margin: 0; 
                padding: 20px;
            }}
            h1 {{
                text-align: center; 
                color: purple; /* First heading in purple */
                padding-bottom: 20px;
            }}
            table {{
                width: 100%; 
                border-collapse: collapse; 
                box-shadow: 0 0 10px rgba(0,0,0,0.1); 
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd; 
                padding: 10px; 
                text-align: left; 
                vertical-align: top;
            }}
            th {{
                background-color: #d0b3e8; /* Changed to darker lavender purple */
                color: #4a4a4a; 
                font-weight: bold;
            }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f1f1f1; }}
            pre {{
                white-space: pre-wrap; 
                word-wrap: break-word; 
                background: #fff; 
                padding: 10px; 
                border: 1px solid #ccc; 
                border-radius: 5px;
                color: black; /* Make text inside sections black */
            }}
            .highlight {{
                font-weight: bold; 
                padding: 3px; 
                border-radius: 3px; 
                display: inline-block; 
            }}
            .highlight-file1 {{ background-color: #DFFFD8; color: green; }}
            .highlight-file2 {{ background-color: #FFDFDF; color: red; }}
        </style>
    </head>
    <body>
        <h1>MV Cells Comparison Report</h1>
        <table>
            <tr>
                <th>Section</th>
                <th>File 1</th>
                <th>File 2</th>
            </tr>
            {"".join(f"<tr><td>{section['title']} #{section['index']}</td><td><pre>{section['highlighted_file1']}</pre></td><td><pre>{section['highlighted_file2']}</pre></td></tr>" for section in sections)}
        </table>
    </body>
    </html>
    """

    with open(output_file_path, "w") as file:
        file.write(html_content)


def main():
    # File paths for comparison
    file1_path = "file1.txt"
    file2_path = "file2.txt"
    
    with open(file1_path) as file1, open(file2_path) as file2:
        file1_content = file1.read()
        file2_content = file2.read()

    # Extracting multiple occurrences of each section from both files
    mv_cells_sections_file1 = extract_multiple_sections(file1_content, "Information: Total number of MV cells in the design")
    mv_cells_sections_file2 = extract_multiple_sections(file2_content, "Information: Total number of MV cells in the design")
    
    report_pst_sections_file1 = extract_multiple_sections(file1_content, "report_pst -verbose")
    report_pst_sections_file2 = extract_multiple_sections(file2_content, "report_pst -verbose")
    
    level_shifters_sections_file1 = extract_multiple_sections(file1_content, "check_level_shifters -verbose")
    level_shifters_sections_file2 = extract_multiple_sections(file2_content, "check_level_shifters -verbose")

    # Prepare sections for the HTML report
    sections = []

    # Add MV Cells sections (matching count of sections between the two files)
    for index, (sec1, sec2) in enumerate(zip(mv_cells_sections_file1, mv_cells_sections_file2)):
        highlighted_file1, highlighted_file2 = highlight_differences(sec1, sec2)
        sections.append({
            "title": "MV Cells Information",
            "index": index + 1,
            "highlighted_file1": highlighted_file1,
            "highlighted_file2": highlighted_file2
        })

    # Add Report PST sections
    for index, (sec1, sec2) in enumerate(zip(report_pst_sections_file1, report_pst_sections_file2)):
        highlighted_file1, highlighted_file2 = highlight_differences(sec1, sec2)
        sections.append({
            "title": "Report PST",
            "index": index + 1,
            "highlighted_file1": highlighted_file1,
            "highlighted_file2": highlighted_file2
        })

    # Add Level Shifters sections
    for index, (sec1, sec2) in enumerate(zip(level_shifters_sections_file1, level_shifters_sections_file2)):
        highlighted_file1, highlighted_file2 = highlight_differences(sec1, sec2)
        sections.append({
            "title": "Check Level Shifters",
            "index": index + 1,
            "highlighted_file1": highlighted_file1,
            "highlighted_file2": highlighted_file2
        })

    # Generate the HTML report
    output_file_path = "mv_cells_comparison_report.html"
    generate_html_report(sections, output_file_path)
    print(f"Comparison report generated: {output_file_path}")


if __name__ == "__main__":
    main()
