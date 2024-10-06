def extract_section(content, start_marker):
    lines = content.splitlines()
    capturing = False
    extracted_lines = []

    for line in lines:
        if start_marker in line:
            capturing = True
        if capturing:
            extracted_lines.append(line)
        if capturing and line.strip() == "1":  # Assumes the section ends at a line containing only "1"
            break
    
    return "\n".join(extracted_lines).strip()

def highlight_differences(text1, text2):
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    max_lines = max(len(lines1), len(lines2))
    highlighted_text = []

    for i in range(max_lines):
        line1 = lines1[i] if i < len(lines1) else ""
        line2 = lines2[i] if i < len(lines2) else ""

        if line1 != line2:
            # Highlight differences in the same pre block
            highlighted_text.append(f"<span style='color:red;'>{line1}</span> <span style='color:blue;'>{line2}</span>")
        else:
            highlighted_text.append(line1)

    return "\n".join(highlighted_text)

def generate_html_report(sections, output_file_path):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>MV Cells Report</title>
        <style>
            body{{font-family:Arial,sans-serif;}}
            table{{width:80%;margin:20px auto;border-collapse:collapse;}}
            th,td{{border:1px solid #ccc;padding:5px;text-align:left;word-wrap:break-word;}}
            th{{background-color:#f2f2f2;width:150px;}}
            pre{{white-space: pre-wrap; word-wrap: break-word;}}
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">MV Cells Comparison Report</h1>
        <table>
            <tr><th>Section</th><th>File 1</th><th>File 2</th></tr>
            {"".join(f"<tr><td>{section['title']}</td><td><pre>{highlight_differences(section['file1'], section['file2'])}</pre></td><td><pre>{highlight_differences(section['file2'], section['file1'])}</pre></td></tr>" for section in sections)}
        </table>
    </body>
    </html>
    """
    
    with open(output_file_path, "w") as file:
        file.write(html_content)

def main():
    file1_path = "file1.txt"
    file2_path = "file2.txt"
    
    with open(file1_path) as file1, open(file2_path) as file2:
        file1_content = file1.read()
        file2_content = file2.read()
    
    sections = [
        {"title": "MV Cells Information", 
         "file1": extract_section(file1_content, "Information: Total number of MV cells in the design"), 
         "file2": extract_section(file2_content, "Information: Total number of MV cells in the design")},
        {"title": "Report PST", 
         "file1": extract_section(file1_content, "report_pst -verbose"), 
         "file2": extract_section(file2_content, "report_pst -verbose")},
        {"title": "Check Level Shifters", 
         "file1": extract_section(file1_content, "check_level_shifters -verbose"), 
         "file2": extract_section(file2_content, "check_level_shifters -verbose")}
    ]
    
    output_file_path = "mv_cells_comparison_report.html"
    generate_html_report(sections, output_file_path)
    print(f"Comparison report generated: {output_file_path}")

if __name__ == "__main__":
    main()

