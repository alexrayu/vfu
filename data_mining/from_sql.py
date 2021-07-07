# Scrapper from mysql/drupal db for companies.

from json import dump
from mysql.connector import (connection)


# Fetch a row values by node id.
def field_values(cursor, nid, field_name, suffix='value'):
    table = 'node__' + field_name
    row = field_name + '_' + suffix
    query = 'SELECT ' + row + ' FROM ' + table + ' WHERE entity_id=' + str(nid)
    cursor.execute(query)
    values = list(cursor.fetchall())
    if (len(values) == 0):
        return None
    if isinstance(values, (tuple, list)):
        for key, value in enumerate(values):
            if isinstance(value, (tuple, list)):
                if len(value) < 2:
                    values[key] = value[0]
                else:
                    values[key] = value
    if isinstance(values, (tuple, list)):
        if len(values) < 2:
            values = values[0]
    if isinstance(values, str):
        values = str(values).strip()
    return values


# Fetch a single text row value (will fetch first if many found).
def image_field_values(cursor, nid, field_name):
    table = 'node__' + field_name
    row = 'delta'
    fields = ['target_id', 'alt', 'title', 'width', 'height']
    for field in fields:
        row += ', ' + field_name + '_' + field
    query = 'SELECT ' + row + ' FROM ' + table + ' WHERE entity_id=' + str(nid)
    cursor.execute(query)
    values = cursor.fetchall()
    if (len(values) == 0):
        return None
    result = None
    if isinstance(values, (tuple, list)):
        result = {}
        for value in values:
            result[value[0]] = {
                'delta': value[0],
            }
            if bool(value[2]): result[value[0]]['alt'] = value[2]
            if bool(value[3]): result[value[0]]['title'] = value[3]
            if bool(value[4]): result[value[0]]['width'] = value[4]
            if bool(value[5]): result[value[0]]['height'] = value[5]

            # Fetch image entity data by id.
            query = 'SELECT * FROM file_managed WHERE fid=' + str(value[1])
            cursor.execute(query, nid)
            file_values = cursor.fetchall()
            file = {}
            columns = [column[0] for column in cursor.description]
            used = ['fid', 'langcode', 'filename', 'uri', 'filemime', 'filesize', 'status', 'type']
            for i, column in enumerate(columns):
                if not column in used: continue
                if isinstance(file_values[0], (tuple, list)):
                    file_value = file_values[0][i]
                    if not isinstance(file_value, (str, int, float)) and bool(file_value):
                        if isinstance(file_value, bytearray): file_value = file_value.decode()
                    if bool(file_value):
                        result[value[0]][column] = file_value

    return result


# Fetch a single text row value (will fetch first if many found).
def terms_field_values(cursor, nid, field_name):
    table = 'node__' + field_name
    row = 'delta'
    fields = ['target_id']
    for field in fields:
        row += ', ' + field_name + '_' + field
    query = 'SELECT ' + row + ' FROM ' + table + ' WHERE entity_id=' + str(nid)
    cursor.execute(query)
    values = cursor.fetchall()
    if (len(values) == 0):
        return None
    result = None
    if isinstance(values, (tuple, list)):
        result = {}
        for value in values:
            result[value[0]] = {
                'delta': value[0],
                'tid': value[1]
            }

            # Fetch image entity data by id.
            query = 'SELECT vid, langcode, name FROM taxonomy_term_field_data WHERE tid=' + str(value[1])
            cursor.execute(query, nid)
            term_values = cursor.fetchone()
            result[value[0]]['vid'] = term_values[0]
            result[value[0]]['langcode'] = term_values[1]
            result[value[0]]['name'] = term_values[2]

    return result


cnx = connection.MySQLConnection(user='drupal', password='drupal',
                                 host='127.0.0.1',
                                 database='ere-src')
cursor = cnx.cursor()
query = 'SELECT nid, title, status, created, changed, langcode FROM node_field_data WHERE type="company"'
cursor.execute(query)
data = {}


# Main node data.
for (nid, title, status, created, changed, langcode) in cursor:
    data[nid] = {
        'nid': nid,
        'title': title,
        'status': status,
        'created': created,
        'changed': changed,
        'langcode': langcode
    }

for key in data:
    node = data[key]
    nid = node['nid']

    # body
    value = field_values(cursor, nid, 'body')
    if value is not None: node['body'] = value

    # field_cka_aid
    value = field_values(cursor, nid, 'field_cka_aid')
    if value is not None: node['cka_aid'] = value

    # field_cka_oid
    value = field_values(cursor, nid, 'field_cka_oid')
    if value is not None: node['cka_oid'] = value

    # field_firma_bildergalerie
    value = image_field_values(cursor, nid, 'field_firma_bildergalerie')
    if value is not None: node['gallery'] = value

    # field_firma_branchen
    value = terms_field_values(cursor, nid, 'field_firma_branchen')
    if value is not None: node['sectors'] = value

    # field_firma_email
    value = field_values(cursor, nid, 'field_firma_email')
    if value is not None: node['email'] = value

    # field_firma_englischer_text
    value = field_values(cursor, nid, 'field_firma_englischer_text')
    if value is not None: node['english_text'] = value

    # field_firma_fax
    value = field_values(cursor, nid, 'field_firma_fax')
    if value is not None: node['fax'] = value

    # field_firma_hausnummer
    value = field_values(cursor, nid, 'field_firma_hausnummer')
    if value is not None: node['house_nr'] = value

    # field_firma_homepage
    value = field_values(cursor, nid, 'field_firma_homepage', 'uri')
    if value is not None: node['website'] = value

    # field_firma_kontaktpersonen
    value = field_values(cursor, nid, 'field_firma_kontaktpersonen', 'target_id')
    if value is not None: node['contacts'] = value

    # field_firma_land
    value = field_values(cursor, nid, 'field_firma_land')
    if value is not None: node['country'] = value

    # field_firma_logos
    value = image_field_values(cursor, nid, 'field_firma_logos')
    if value is not None: node['logos'] = value

    # field_firma_namenszusatzzeile
    value = field_values(cursor, nid, 'field_firma_namenszusatzzeile')
    if bool(value): node['slogan'] = value

    # field_firma_niederlassungen
    value = terms_field_values(cursor, nid, 'field_firma_niederlassungen')
    if value is not None: node['offices'] = value

    # field_firma_notizen
    value = field_values(cursor, nid, 'field_firma_notizen')
    if bool(value): node['notes'] = value

    # field_firma_ort
    value = field_values(cursor, nid, 'field_firma_ort')
    if bool(value): node['city'] = value

    # field_firma_postleitzahl
    value = field_values(cursor, nid, 'field_firma_postleitzahl')
    if bool(value): node['zip'] = value

    # field_firma_postleitzahl
    value = field_values(cursor, nid, 'field_firma_postleitzahl')
    if bool(value): node['zip'] = value

    # field_firma_rubriken
    value = terms_field_values(cursor, nid, 'field_firma_rubriken')
    if value is not None: node['categories'] = value

    # field_firma_shortlink
    value = field_values(cursor, nid, 'field_firma_shortlink')
    if bool(value): node['shortlink'] = value

    # field_firma_strasse
    value = field_values(cursor, nid, 'field_firma_strasse')
    if bool(value): node['street'] = value

    # field_firma_telefon
    value = field_values(cursor, nid, 'field_firma_telefon')
    if bool(value): node['phone'] = value

    # node__field_firma_veroeffentlichen_am
    value = field_values(cursor, nid, 'field_firma_veroeffentlichen_am')
    if bool(value): node['publish_from'] = value

    # field_firma_telefon
    value = field_values(cursor, nid, 'field_firma_veroeffentlichen_bis')
    if bool(value): node['publish_to'] = value

    data[key] = node


# Get the email.


cursor.close()
cnx.close()

with open('companies.json', 'w') as outfile:
    dump(data, outfile, indent=2, separators=(',', ': '))

print('Saved {0} records to "companies.json".' . format(len(data)))