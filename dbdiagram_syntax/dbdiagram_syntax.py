import os


if __name__ == '__main__':

    """
    This is a complementary program to the psql_ops/create_diagram/create_diagram.py file. That file creates
    table syntax for sql in the form of txt files. This script will edit those txt files
    so that they are more akin to the syntax of dbdiagram.io.

    This script will collect all txt files in the directory input, and
    edit them to approximate the syntax for tables in db diagram.

    """

    txts_location = input("Input the path where txt files are stored: ")

    db_diagram_location = input("Input the path where the new dbdiagram txt files will be stored: ")

    os.chdir(txts_location)

    txts = [x for x in os.listdir() if x.endswith('.txt') == True]

    for i in txts:

        with open(i) as f:
            txt = f.read()

        txt_new = txt.replace('"', '')
        txt_new = txt_new.replace('double precision', 'int')
        txt_new = txt_new.replace(',', '')
        txt_new = txt_new.replace('PRIMARY KEY', '[pk]')
        txt_new = txt_new.replace('CREATE ', '')
        txt_new = txt_new.replace('(', '{')
        txt_new = txt_new.replace(')', '}')
        txt_new = txt_new.replace(';', '')

        with open(db_diagram_location + '/dbdiagram_' + i, 'w') as f:
            f.write(txt_new)
