import json
import datetime


# -- get data from db
def get_data(connection, filter_word, padlist_paged):
  try:
    with connection.cursor() as cursor:
        # due to the way etherpad uses sql (eg, by dumping in in table with two columns all data, simply mapping the k,v json structure to sql)
        # it takes too much time and computation to keep in memory all the pads and then filter them in python
        # therefore:
        # - get correct pad and fetch num of authors and of revisions (['head']: <num>)
        # - fetch correct pad-revs-<num> to get timestamp

        pad_list = []
        # TODO  run more efficient query?
        # see <https://stackoverflow.com/questions/5803472/sql-where-id-in-id1-id2-idn>
        for pad in padlist_paged:
          try:
            sql_pad_value = "SELECT DISTINCT store.value FROM store WHERE store.key = %s"
            cursor.execute(sql_pad_value, ('pad:' + pad,))

            pad_value = json.loads(cursor.fetchone()['value'])
            pad_text = pad_value['atext']['text']

            # if pad_text.split('\n')[0] != filter_word:
            if filter_word not in pad_text:
              # -- title
              pad_title = pad

              # -- revision num
              pad_revisions = pad_value['head']

              # -- author num
              pad_authors = 0
              for item in pad_value['pool']['numToAttrib'].values():
                if item[0] == 'author':
                  pad_authors += 1

              # -- timestamp
              sql_pad_rev = "SELECT DISTINCT store.value FROM store WHERE store.key = %s"
              cursor.execute(sql_pad_rev, ('pad:' + pad + ':revs:' + str(pad_value['head']),))

              ts = json.loads(cursor.fetchone()['value'])['meta']['timestamp']
              pad_timestamp = datetime_format(ts)

              # make tuple out of pad keys
              pad_item = (pad_title, pad_timestamp, pad_revisions, pad_authors)

              # -- add to list
              pad_list.append(pad_item)

          except Exception as e:
            print('parse pad err =>', e)

        return pad_list

  except Exception as e:
    print('db err =>', e)

  finally:
    cursor.close()




def datetime_format(timestamp):
  # <https://stackoverflow.com/a/31548402>
  # divide by /1000 to convert from milliseconds to seconds
  ts = timestamp / 1000
  
  # <https://stackoverflow.com/a/37188257>
  ts = datetime.datetime.utcfromtimestamp(ts)
  
  # <https://stackoverflow.com/a/46339491>
  ts = ts.replace(tzinfo=datetime.timezone.utc)
  ts = ts.astimezone().strftime('%Y-%m-%d %H:%M:%S')
  
  return ts
