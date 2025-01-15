"""
CSV to BibTeX Converter Script
--------------------------------
This Python script converts bibliographic data from a CSV file into BibTeX format, making it suitable for use with citation managers like Zotero or JabRef. It focuses on the "Article" reference type but can be extended to support other types as needed.

Features:
- Flexible handling of CSV fields with default fallbacks for missing data.
- Automatic generation of BibTeX keys based on author names and publication years.
- Error handling for missing or incomplete rows.

Usage:
To run the script, use the following Python command in your terminal:

```bash
python csv2bib.py input.csv output.bib
```

Replace `input.csv` with the path to your CSV file containing bibliographic data and `output.bib` with the desired output file path for the BibTeX file.
"""

import csv

def generate_bibtex_key(authors, year):
    """
    Generate a BibTeX key from the first author's last name and the year.
    """
    last_names = authors.split(",")[0].split()
    last_name = last_names[-1] if last_names else "unknown"
    return f"{last_name.lower()}{year}"

def convert_csv_to_bibtex(csv_file, bibtex_file):
    """
    Convert a CSV file to BibTeX format.

    Parameters:
        csv_file (str): Path to the input CSV file.
        bibtex_file (str): Path to the output BibTeX file.
    """
    with open(csv_file, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        with open(bibtex_file, "w", encoding="utf-8") as bibtexfile:
            for row in reader:
                try:
                    authors = row.get("Authors", "Unknown").strip()
                    year = row.get("Year", "n.d.").strip()
                    title = row.get("Title", "Untitled").strip()
                    source_title = row.get("Source title", "Unknown").strip()
                    volume = row.get("Volume", "").strip()
                    page_start = row.get("Page start", "").strip()
                    page_end = row.get("Page end", "").strip()
                    pages = f"{page_start}-{page_end}" if page_start and page_end else ""
                    doi = row.get("DOI", "").strip()
                    bibtex_key = generate_bibtex_key(authors, year)

                    bibtex_entry = (
                        f"@article{{{bibtex_key},\n"
                        f"  author = {{{authors}}},\n"
                        f"  title = {{{title}}},\n"
                        f"  year = {{{year}}},\n"
                        f"  journal = {{{source_title}}},\n"
                        f"  volume = {{{volume}}},\n"
                        f"  pages = {{{pages}}},\n"
                        f"  doi = {{{doi}}}\n"
                        f"}}\n\n"
                    )
                    bibtexfile.write(bibtex_entry)
                except KeyError as e:
                    print(f"Missing expected column: {e}")
                except Exception as e:
                    print(f"Error processing row: {row}\n{e}")

if __name__ == "__main__":
    convert_csv_to_bibtex("input.csv", "output.bib")
