import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

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

def parse_input_file(filename):
    with open(filename, 'r', encoding='utf-16') as f:
        lines = f.readlines()

    groups = []  # Список всех групп
    group_stack = []  # Стек для вложенных групп
    current_group = None  # Текущая группа
    current_entry = None  # Текущая запись
    notes_lines = []  # Буфер для строк Notes
    is_notes = False  # Флаг, что мы находимся в блоке Notes
    notes_line_count = 0
    line_index = 0
    before_line = None
    for line in lines:
        line = line.strip()

        if notes_line_count == 0:
            if is_notes:
                # Если это конец Notes, добавляем их в запись
                current_entry['fields']['Notes'] = '\n'.join(notes_lines)
                notes_lines = []
                is_notes = False
                current_group['entries'].append(current_entry)
                current_entry = None
            else:
                # Обработка пустых строк
                if not line:
                    if current_entry:
                        # Если это конец записи, добавляем её в текущую группу
                        current_group['entries'].append(current_entry)
                        current_entry = None
                    elif before_line:
                        if group_stack:
                            # Если есть родительская группа, добавляем текущую группу в неё
                            parent_group = current_group
                            parent_group['groups'].append({'name': before_line, 'groups': [], 'entries': []})
                            current_group = parent_group['groups'][-1]
                        else:
                            # Иначе создаем новую группу
                            current_group = {'name': before_line, 'groups': [], 'entries': []}
                            group_stack.append(current_group)
                        # continue
                    else:
                        # Если это конец группы, добавляем её в родительскую группу
                        if group_stack:
                            current_group = parent_group

                # Обработка новой записи
                else:
                    # Обработка строк с ключами
                        if ':' in line:
                            if not current_entry :
                                current_entry = {'title': before_line, 'fields': {}}
                            # else:
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

        # Обработка записей
        for entry in group['entries']:
            entry_elem = ET.SubElement(group_elem, 'Entry')
            string_elem = ET.SubElement(entry_elem, 'String')
            ET.SubElement(string_elem, 'Key').text = 'Title'
            ET.SubElement(string_elem, 'Value').text = entry['title']

            for key, value in entry['fields'].items():
                string_elem = ET.SubElement(entry_elem, 'String')
                ET.SubElement(string_elem, 'Key').text = key
                ET.SubElement(string_elem, 'Value').text = value

        # Рекурсивная обработка вложенных групп
        if group['groups']:
            create_kp_xml(group['groups'], group_elem)

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