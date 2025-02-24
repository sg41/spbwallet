#
# Code to Convert Spb Wallet TXT export file to KeePass XML import file.
#
# Original Author: Gerald Naveen A (http://geraldnaveen.blogspot.com)
#
# License:
# You are free to modify/distribute/use for commercial/non-commercial/
# personal applications. Any modification to this code needn't be published.
# However, any publication of this code or the derivative of this code, should
# include the original author and this license text.
#

import sys


def mywrite(f, str):
    f.write("{0}\n".format(str))


def main():
    print("\nSpb Wallet to KeePass Convertor v 1.0 by Gerald Naveen\n")
    print("Report bugs at http://geraldnaveen.blogspot.com/2010/11/myapp-spb-wallet-to-keepass-convertor.html\n")
    if len(sys.argv) < 3:
        print("Usage: spb_wallet_to_keepass.py <spb_txt_export_file> <keepass_xml_import_file>")
        print(
            "\nWhere,\nspb_txt_export_file: path to the TXT file exported from Spb Wallet.")
        print("keepass_txt_import_file: path to the output XML file, that shall be imported into KeePass.")
        return

    try:
        # Open input file in text mode with UTF-8 encoding
        with open(sys.argv[1], 'r', encoding='windows-1251') as ifile:
            # Open output file in write mode
            with open(sys.argv[2], 'w') as ofile:

                FOLDER_NAME_TOKEN = 1
                ENTRY_NAME_TOKEN = FOLDER_NAME_TOKEN + 1
                BEFORE_NOTES_TOKEN = ENTRY_NAME_TOKEN + 1
                NOTES_TOKEN = BEFORE_NOTES_TOKEN + 1
                INVALID_VALUE = 'invalid'

                next_token = ENTRY_NAME_TOKEN
                folder_name = INVALID_VALUE
                entry_name = INVALID_VALUE
                user_name = INVALID_VALUE
                password = INVALID_VALUE
                url = INVALID_VALUE
                notes = INVALID_VALUE
                valid_entry = False

                mywrite(
                    ofile, '<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
                mywrite(ofile, '<pwlist>')

                for line in ifile:
                    line = line.strip('\r\n')
                    if len(line) == 0:
                        # empty line
                        if valid_entry == False:
                            # entry name found after folder name
                            folder_name = entry_name
                            entry_name = INVALID_VALUE
                        else:
                            # found the last line of the entry..dump
                            mywrite(ofile, '<pwentry>')
                            if folder_name != INVALID_VALUE:
                                mywrite(
                                    ofile, '<group>{0}</group>'.format(folder_name))
                            mywrite(
                                ofile, '<title>{0}</title>'.format(entry_name))
                            if user_name != INVALID_VALUE:
                                mywrite(
                                    ofile, '<username>{0}</username>'.format(user_name))
                            if password != INVALID_VALUE:
                                mywrite(
                                    ofile, '<password>{0}</password>'.format(password))
                            if url != INVALID_VALUE:
                                mywrite(ofile, '<url>{0}</url>'.format(url))
                            if notes != INVALID_VALUE:
                                notes = notes.replace('\n', '&#xD;&#xA;')
                                mywrite(
                                    ofile, '<notes>{0}</notes>'.format(notes))
                            mywrite(ofile, '</pwentry>')
                            user_name = INVALID_VALUE
                            password = INVALID_VALUE
                            url = INVALID_VALUE
                            notes = INVALID_VALUE
                        valid_entry = False
                        next_token = ENTRY_NAME_TOKEN
                    else:
                        if next_token == ENTRY_NAME_TOKEN:
                            entry_name = line
                            next_token = BEFORE_NOTES_TOKEN
                        else:
                            valid_entry = True
                            if next_token == BEFORE_NOTES_TOKEN:
                                if line.startswith('User Name:'):
                                    user_name = line[len(
                                        'User Name:'):].strip(' ')
                                elif line.startswith('Password:'):
                                    password = line[len(
                                        'Password:'):].strip(' ')
                                elif line.startswith('Web Site:'):
                                    url = line[len('Web Site:'):].strip(' ')
                                elif line.startswith('Notes:'):
                                    if notes == INVALID_VALUE:
                                        notes = line[len('Notes:'):].strip(' ')
                                    else:
                                        notes += '\n' + \
                                            line[len('Notes:'):].strip(' ')
                                    next_token = NOTES_TOKEN
                                else:
                                    # any unknown params should go as notes.
                                    if notes == INVALID_VALUE:
                                        notes = line
                                    else:
                                        notes += '\n' + line
                            elif next_token == NOTES_TOKEN:
                                # any thing from the notes section.
                                notes += '\n' + line

                mywrite(ofile, '</pwlist>')

    except Exception as e:
        print("Unknown error occured while processing the input file.")
        print(e)

    print("Success. Now import {0} in KeePass as KeePass XML".format(
        sys.argv[2]))


if __name__ == "__main__":
    main()
