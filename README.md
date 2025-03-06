# SpbWallet to KeePass2 XML Converter

This Python script converts export files from **SpbWallet** into the KeePass2 XML format (.xml).  **SpbWallet** was a popular password manager for mobile devices, particularly prevalent before widespread cloud-based solutions.  **KeePass 2** is a free, open-source, lightweight, and easy-to-use password manager for Windows, macOS, Linux, and other operating systems. This converter allows users migrating away from SpbWallet to import their password data into the widely-used and secure KeePass2 password manager, preserving group hierarchy and entries with various fields, including notes.

## Features

*   Converts text-based password data from SpbWallet export files to KeePass XML format.
*   Supports group hierarchy and nested groups from SpbWallet data.
*   Handles entries with fields like Username, Password, URL, and custom fields exported from SpbWallet.
*   Supports multi-line "Notes" field from SpbWallet entries.
*   Translates common Russian/English key names from SpbWallet to standard KeePass field names (e.g., "Пользователь" to "UserName").
*   Command-line interface for easy usage.
*   Customizable input and output file encodings.

## Usage

To use the script, you need to have Python installed.  Run the script from the command line:

```bash
python script_name.py [input_file] [output_file] [--input_encoding <encoding>] [--output_encoding <encoding>]
```

*   `script_name.py`:  Replace this with the actual name of your Python script file (e.g., `spbwallet_to_keepass.py`).
*   `input_file` (optional): Path to the SpbWallet export text file. If not provided, defaults to `input.txt`.
*   `output_file` (optional): Path to the output KeePass XML file. If not provided, defaults to `output.xml`.
*   `--input_encoding <encoding>` (optional): Encoding of the input file. Defaults to `utf-16`. Common encodings are `utf-8`, `utf-16`, `cp1251` etc.
*   `--output_encoding <encoding>` (optional): Encoding of the output XML file. Defaults to `utf-8`.

**Examples:**

*   Convert `spbwallet_export.txt` (UTF-8 encoded) to `keepass_database.xml` (UTF-8 encoded):
    ```bash
    python script_name.py spbwallet_export.txt keepass_database.xml --input_encoding utf-8
    ```

*   Convert `data.txt` (default UTF-16 encoded) to `output.xml` (default UTF-8 encoded):
    ```bash
    python script_name.py data.txt
    ```

*   Convert `input.txt` (default UTF-16 encoded) to `result.xml` (UTF-8 encoded):
    ```bash
    python script_name.py input.txt result.xml
    ```

## Input File Format

**This script is specifically designed to process export files from the SpbWallet program.** The input text file should be structured as follows:

*   Groups and Entries: The file is organized into groups and entries, mirroring the SpbWallet structure. Groups can be nested.
*   Group Names: A group name is indicated by a line containing the group's name.
*   Entries within a Group: Entries belonging to a group follow the group name.
*   Entry Title: The first non-empty line after a group name (or after the previous entry) is considered the title of a new entry.
*   Entry Fields:  Entry fields are defined in the format `Key: Value`. Each field should be on a new line.
*   Notes Field: The "Notes" field is a special field that can span multiple lines. It starts with `Notes: Value` and continues until the next blank line or the start of a new entry/group.
*   Blank Lines:
    *   A single blank line separates entries within a group.
    *   Two or more blank lines can separate groups or indicate the end of a group and potentially the start of a new top-level group if a group name line follows.

**Example Input File Structure:**

```text
Group 1
Entry Title 1
UserName: user1
Password: password1
URL: http://example.com
Notes: This is a note for entry 1.
It can be multi-line.

Entry Title 2
UserName: user2
Password: password2

Group 2

Subgroup 1
Entry in Subgroup 1
UserName: subuser1
Password: subpassword1


Entry in Group 2
UserName: group2user
Password: group2password
```

In this example:

*   "Group 1" and "Group 2" are top-level groups.
*   "Subgroup 1" is nested within "Group 2".
*   "Entry Title 1" and "Entry Title 2" are entries in "Group 1".
*   "Entry in Subgroup 1" is in "Subgroup 1".
*   "Entry in Group 2" is directly in "Group 2".

## Dependencies

*   Python Standard Library: The script relies on standard Python libraries (`xml.etree.ElementTree`, `xml.dom.minidom`, `re`, `argparse`). No external libraries need to be installed.

## Potential Improvements

*   Error Handling: Implement more robust error handling for file operations and input parsing.
*   Input Format Flexibility:  While designed for SpbWallet, consider making the input format more flexible and configurable, potentially supporting different delimiters or structured formats.
*   Input Data Validation: Add validation to check the input data for correctness and consistency, especially for SpbWallet export format variations.
*   Enhanced KeePass XML Features:  Extend the script to support more advanced KeePass XML features like icons, timestamps, and custom data attributes, potentially mapping SpbWallet specific data if applicable.
*   Improved Notes Handling:  Refine the regular expression for detecting the end of the "Notes" block for better performance and robustness.

## Known Issues

*   **Group Hierarchy Parsing Imperfections:** Due to limitations in the SpbWallet export file format, specifically the lack of explicit group delimiters, the script may not always perfectly reconstruct the original group hierarchy.  This is most noticeable when a group's last entry is followed by a multi-line "Notes" block. In such cases, the script might misinterpret the end of the group, potentially leading to entries or subsequent groups being placed in the wrong parent group. Please review the generated XML file to ensure the group structure is as expected, especially if your SpbWallet data heavily relies on nested groups and extensive use of the "Notes" field at the end of groups.

## License

[MIT License](LICENSE)

## Author

[Serge Gorbatenko](https://github.com/sg41)
