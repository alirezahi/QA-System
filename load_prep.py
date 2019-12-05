f = open('static/file/prep.txt')
for line in f:
    if line != '':
        PrePosition.objects.get_or_create(text=line.strip('\n'))
