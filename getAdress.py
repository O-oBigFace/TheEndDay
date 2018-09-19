

for eachline in f.readlines():
    js = None
    MAX_RETRY = 0

    while js is None and MAX_RETRY < 5:
        MAX_RETRY += 1
        if MAX_RETRY > 1:
            time.sleep(MAX_RETRY)
        payloads = {
        'sensor': 'false',
        'address': eachline,
        }

        if MAX_RETRY < 4:
            c = requests.get(serviceurl, proxies=proxies, params=payloads, verify=False)
        else:
            c = requests.get(serviceurl, params=payloads)

        data = c.text

        try:
            js = json.loads(data)
        except:
            continue

        if js is None or 'status' not in js or js['status'] != 'OK':
            print('===Failed To Retrieve===', 'retry = ', MAX_RETRY)
            js = None

    if js is None:
        print('ERROR\n')
        f_res.write('\n')
        continue

    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    # print('lat:', lat, 'lng:', lng)
    location = js['results'][0]['formatted_address']
    # print(location)
    res =  '\"' + location + '\" | ' + str(lat) + ' | ' + str(lng) + ' | ' + '\n'
    print(res)
    f_res.write(res)