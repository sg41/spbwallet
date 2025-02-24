import re


def process_entry(entry_text):
    lines = entry_text.strip().split('\n')
    group = lines[0].strip()  # First line is the group
    # Second line is the owner (if present)
    owner = lines[1].strip() if len(lines) > 1 else ""

    title_parts = []
    for i in range(2, len(lines)):
        line = lines[i].strip()
        if line.startswith(('Номер:', 'Card #:', 'Card Number:')):
            title_parts.append(line.split(":")[1].strip())
            continue
        if line.startswith('Владелец:'):
            title_parts.append(line.split(":")[1].strip())
            continue
        if line.startswith('Owner:'):
            title_parts.append(line.split(":")[1].strip())
            continue
        if len(line) > 0:
            # Append other non-empty lines to the title
            title_parts.append(line)

    title = " ".join(title_parts)
    title = title.strip()
    if owner:
        title = title + f" ({owner})"

    notes_str = ""
    password = ""
    username = ""
    url = ""

    for line in lines[2:]:
        parts = line.split(":", 1)  # Split line into key:value pair
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            if key in ['PIN', 'Password', 'Пароль']:
                password = value
            elif key in ['Владелец:', 'Owner:', 'User Name:', 'Пользователь:', 'Username:', 'Номер:', 'Card #:', 'Card Number:', 'Name:', 'Имя:', 'Email:', 'Эл. почта:', 'Эл. почта сл. поддержки:']:
                continue  # these values are added elsewhere
            elif key.startswith('Notes:'):
                notes_str = value
            else:
                notes_str += f"{key}: {value}\n"

    notes_str = notes_str.strip()
    return group, title, username, password, url, notes_str


def main():
    try:
        with open('input.txt', 'r', encoding='windows-1251') as infile, open('output.xml', 'wt', encoding='windows-1251') as outfile:
            outfile.write(
                '<?xml version="1.0" encoding="windows-1251" standalone="yes"?>\n')
            outfile.write('<pwlist>\n')

            entry_text = ""
            for line in infile:
                line = line.strip()
                if len(line) == 0:  # Empty line separates entries
                    group, title, username, password, url, notes = process_entry(
                        entry_text)
                    outfile.write(f'<pwentry>\n')
                    outfile.write(f'<group>{group}</group>\n')
                    outfile.write(f'<title>{title}</title>\n')
                    if username:
                        outfile.write(f'<username>{username}</username>\n')
                    if password:
                        outfile.write(f'<password>{password}</password>\n')
                    if url:
                        outfile.write(f'<url>{url}</url>\n')
                    if notes:
                        outfile.write(f'<notes>{notes}</notes>\n')
                    outfile.write(f'</pwentry>\n')
                    entry_text = ""
                else:
                    entry_text += line + '\n'

            # Process the last entry
            if entry_text:
                group, title, username, password, url, notes = process_entry(
                    entry_text)
                outfile.write(f'<pwentry>\n')
                outfile.write(f'<group>{group}</group>\n')
                outfile.write(f'<title>{title}</title>\n')
                if username:
                    outfile.write(f'<username>{username}</username>\n')
                if password:
                    outfile.write(f'<password>{password}</password>\n')
                if url:
                    outfile.write(f'<url>{url}</url>\n')
                if notes:
                    outfile.write(f'<notes>{notes}</notes>\n')
                outfile.write(f'</pwentry>\n')

            outfile.write('</pwlist>\n')

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
