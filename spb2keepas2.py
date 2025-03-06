import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import argparse

def translate_key(key):
    translations = {
        'Пользователь': 'UserName',
        'User Name': 'UserName',
        'Пароль': 'Password',
        'Вебсайт': 'URL',
        'Сайт': 'URL',
        'Web Site': 'URL',
    }
    return translations.get(key, key)

def parse_input_file(filename, input_encoding='utf-16'):
    with open(filename, 'r', encoding=input_encoding) as f:
        lines = f.readlines()

    group_stack = []  # Stack for nested groups
    current_group = None  # Current group
    current_entry = None  # Current entry
    notes_lines = []  # Buffer for Notes lines
    is_notes = False  # Flag indicating if we are in a Notes block
    notes_line_count = 0
    line_index = 0
    before_line = None
    for line in lines:
        line = line.strip()

        if notes_line_count == 0:
            if is_notes:
                # If it is the end of Notes, add them to the entry
                current_entry['fields']['Notes'] = '\n'.join(notes_lines)
                notes_lines = []
                is_notes = False
                # End of Notes always means the end of an entry
                current_group['entries'].append(current_entry)
                current_entry = None
            else:
                # Processing empty lines
                if not line:
                    if current_entry:
                        # If it is the end of an entry, add it to the current group
                        current_group['entries'].append(current_entry)
                        current_entry = None
                    elif before_line: # non empty line followed by empty line is a group name
                        if group_stack:
                            # If there is a parent group, add the current group to it
                            parent_group = current_group
                            parent_group['groups'].append({'name': before_line, 'groups': [], 'entries': []})
                            current_group = parent_group['groups'][-1]
                        else:
                            # Otherwise create a new group
                            current_group = {'name': before_line, 'groups': [], 'entries': []}
                            group_stack.append(current_group)
                    else:
                        # If it is the end of a group
                        if group_stack:
                            current_group = parent_group

                else:
                    # Processing lines with keys
                    if ':' in line:
                        if not current_entry :
                            # Create a new entry
                            current_entry = {'title': before_line, 'fields': {}}

                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()

                        if key == 'Notes':
                            is_notes = True
                            notes_lines.append(value)

                            rest_of_the_file = ''.join(lines[line_index:])
                            match = re.search(r'(\n\n^[^:\n]+\n.+:\s.+)|(\n\n\n^[^:\n]+\n\n)',  rest_of_the_file, re.MULTILINE)
                            if match:
                                notes_end=match.start()+1
                                notes_line_count = match.string[:notes_end].count('\n')-1
                        else:
                            current_entry['fields'][translate_key(key)] = value
        else:
            notes_lines.append(line)
            notes_line_count -= 1

        line_index += 1
        before_line = line

    return group_stack

def create_kp_xml(groups, parent_group_elem=None):
    root = None
    if parent_group_elem is None:
        root = ET.Element('KeePassFile')
        meta = ET.SubElement(root, 'Meta')
        ET.SubElement(meta, 'Generator').text = 'KeePass2 XML Generator'
        root_group = ET.SubElement(ET.SubElement(root, 'Root'), 'Group')
        ET.SubElement(root_group, 'Name').text = 'Root'
        parent_group_elem = root_group

    for group in groups:
        group_elem = ET.SubElement(parent_group_elem, 'Group')
        ET.SubElement(group_elem, 'Name').text = group['name']

        # Entry processing
        for entry in group['entries']:
            entry_elem = ET.SubElement(group_elem, 'Entry')
            string_elem = ET.SubElement(entry_elem, 'String')
            ET.SubElement(string_elem, 'Key').text = 'Title'
            ET.SubElement(string_elem, 'Value').text = entry['title']

            for key, value in entry['fields'].items():
                string_elem = ET.SubElement(entry_elem, 'String')
                ET.SubElement(string_elem, 'Key').text = key
                ET.SubElement(string_elem, 'Value').text = value

        # Recursive processing of nested groups
        if group['groups']:
            create_kp_xml(group['groups'], group_elem)

    return root

def save_xml(xml_root, filename, output_encoding='utf-8'):
    xml_str = ET.tostring(xml_root, encoding=output_encoding)
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding=output_encoding).decode(output_encoding)

    with open(filename, 'w', encoding=output_encoding) as f:
        f.write(pretty_xml)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input_file', nargs='?', default='input.txt')
    argparser.add_argument('output_file', nargs='?', default='output.xml')
    argparser.add_argument('--input_encoding', default='utf-16', help='Input file encoding')
    argparser.add_argument('--output_encoding', default='utf-8', help='Output file encoding')
    args = argparser.parse_args()

    groups = parse_input_file(args.input_file, args.input_encoding)
    xml_root = create_kp_xml(groups)
    save_xml(xml_root, args.output_file, args.output_encoding)
    
    print(f"File {args.input_file} successfully converted to {args.output_file}")