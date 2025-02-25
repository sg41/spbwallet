import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

def parse_input_file(filename):
    with open(filename, 'r', encoding='utf-16') as f:
        content = f.read()
    
    groups = []
    current_group = None
    current_entry = None
    entries = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_entry:
                if notes:
                    current_entry['fields']['Notes'] = '\n'.join(notes)
                    notes = []
                entries.append(current_entry)
                current_entry = None
            continue
        
        # if re.match(r'^[А-ЯЁ][а-яё ]+$', line) and not current_entry and not current_group:
        if re.match(r'^[^:]+$', line) and not current_entry and not current_group:
            if current_group:
                groups.append(current_group)
            current_group = {'name': line, 'entries': []}
            entries = []
            continue
        
        if not current_group:
            continue
        
        if not current_entry:
            current_entry = {'title': line, 'fields': {}}
            notes = []
        else:
            if ': ' in line:
                key, val = line.split(': ', 1)
                current_entry['fields'][key] = val
            else:
                notes.append(line)
    
    if current_entry:
        if notes:
            current_entry['fields']['Notes'] = '\n'.join(notes)
        entries.append(current_entry)
    if current_group:
        current_group['entries'] = entries
        groups.append(current_group)
    
    return groups

def create_kp_xml(groups):
    root = ET.Element('KeePassFile')
    root_group = ET.SubElement(ET.SubElement(root, 'Root'), 'Group')
    ET.SubElement(root_group, 'Name').text = 'Root'
    
    for group in groups:
        group_elem = ET.SubElement(root_group, 'Group')
        ET.SubElement(group_elem, 'Name').text = group['name']
        
        for entry in group['entries']:
            entry_elem = ET.SubElement(group_elem, 'Entry')
            
            # Title field
            title = entry['title']
            string_elem = ET.SubElement(entry_elem, 'String')
            ET.SubElement(string_elem, 'Key').text = 'Title'
            ET.SubElement(string_elem, 'Value').text = title
            
            # Other fields
            fields = entry['fields']
            for key, value in fields.items():
                string_elem = ET.SubElement(entry_elem, 'String')
                ET.SubElement(string_elem, 'Key').text = key
                ET.SubElement(string_elem, 'Value').text = value
    
    return root

def save_xml(xml_root, filename):
    xml_str = ET.tostring(xml_root, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='utf-8').decode('utf-8')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == '__main__':
    groups = parse_input_file('input.txt')
    xml_root = create_kp_xml(groups)
    save_xml(xml_root, 'keepass_output.xml')
    print("Файл успешно преобразован в keepass_output.xml")