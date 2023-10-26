a = [{'id':1,'name':'fff'},{'id':2,'name':'fff'},{'id':3,'name':'fff'}]
b = [1,2]
for item in a:
    if item.get('id') in b:
        item['is_select'] = 't'
    else:
        item['is_select'] = 'f'

print(a)