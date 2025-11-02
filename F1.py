import requests
# test
def analizet_brauceju_overtakes(driver_number, session_key=None):
    url = f"https://api.openf1.org/v1/overtakes"

    parametrs = {"overtaking_driver_number": driver_number, "position": 1}
    if session_key:
        parametrs["sessions_key"] = session_key

    try:
        r = requests.get(url, params=parametrs)     #
    except Exception as e:
        print(f"Kļūda pieprasot datus no API: {e}")
        return 0, False, None

    if r.status_code != 200:
        print(f"Kļūda pieprasot datus no API: {r.status_code}")
        return 0, False, None

    results =r.json()
    count = len (results)   #
    gadi = []         #

    for it in results:
        d = it.get("date")
        if d:
            try:
                gadi.append(int(d[:4]))   #
            except:
                pass

    last_year = max(gadi) if gadi else None   #
    active = (last_year is not None and last_year >= 2025)   #

    return count, active, last_year   
        
response = requests.get("https://api.openf1.org/v1/drivers")
#print(response.text) 
response.status_code
if response.status_code == 200:
    drivers = response.json()

    print("Formula 1 drivers:")

    print("\nPirmie 15 braucēji:")
    for driver in drivers[:15]:
        print(f"{driver['driver_number']}: {driver['full_name']}")
    def find_driver(num):                   #
        return next((d for d in drivers if str(d.get("driver_number")) == str(num)), None)    #
    
    def get_valid_driver(prompt):      #
        while True:
            a = input(prompt).strip()   #
            entry = find_driver(a)
            if entry:                #
                return a, entry
            print("Braucējs ar šadu numuru netika atrasts. Meģini velreiz.")
    
    print("\nSalidzinasana braucejus")
    b_num, b_entry = get_valid_driver("\nIevadi pirmo brauceja numuru - ")
    c_num, c_entry = get_valid_driver("\nIevadi otro brauceja numuru -")

    def saglabat_attelu(entry):
        url = entry.get("headshot_url")
        if url and url.startswith("http"):
            img_data = requests.get(url).content
            faila_vards = f"{entry['full_name'].replace(' ', '_')}.png"
            with open(faila_vards, "wb") as f:
                f.write(img_data)
            return faila_vards
        else:
            return "Nav attēla datu"

    b_picture = saglabat_attelu(b_entry)
    c_picture = saglabat_attelu(c_entry)

    b_count, b_year, b_active = analizet_brauceju_overtakes(b_num)
    c_count, c_year, c_active = analizet_brauceju_overtakes(c_num)
    
    print()
    print(f"{b_entry['full_name']} ({b_entry.get('team_name','Nav datu')}) - Uzvaras: {b_count}, Pēdējais gads: {b_year}, Aktīvs: {'Jā' if b_active else 'Nē'}, Attels - {b_picture}")  #
    print(f"{c_entry['full_name']} ({c_entry.get('team_name','Nav datu')}) - Uzvaras: {c_count}, Pēdējais gads: {c_year}, Aktīvs: {'Jā' if c_active else 'Nē'}, Attels - {c_picture}")  #
    
    if b_count > c_count:
        print(f"\n{b_entry['full_name']} ir vairak reizu uzvreja. ({b_count} > {c_count})")
    elif b_count <c_count:
        print(f"\n{c_entry['full_name']} ir vairak reizu uzvareja. ({c_count} > {b_count})") 
    else:
        print("\nAbiem braucejiem ir uzvaresanas skaits")