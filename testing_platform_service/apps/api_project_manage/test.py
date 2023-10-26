params =[{'id': '9', 'name': 'ccccccc', 'code': '啛啛喳喳'}, '9']
field_set = ''
for item in params[0]:
    print('item===', item)
    field_set += f"{item} = {str(params[0][item])}, "

print(field_set)