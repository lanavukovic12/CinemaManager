from datetime import datetime, timedelta

users = []  # korisnicko ime, lozinka, ime, prezime, uloga
films = []  # naziv,zanr,trajanje,reziser,glavni glumci,zemlja porekla, godina proizvodnje
projections = []  # sifra, sala, vreme pocetka, vreme kraja, dani prikazivanja, naziv filma, cena
projection_times = []  # sifra,datum
halls = []  # sifra, ime, broj redova, broj sedista u redu
tickets = []  # id, Ime i prezime, userid, termin projekcije, oznaka sedista, datum prodaje, rez/kupljena -> 0/1
loyalty_cards = []  # user_id, vreme izrade kartice
sales = []  # ticket_id, cena, id_prodavca, datum_prodaje


def unpack(filename):
    nfile = open(filename, "r")
    files = []
    file_data = nfile.readline()
    while file_data != "":
        user = file_data.replace("\n", "").split("|")
        files.append(user)
        file_data = nfile.readline()
    nfile.close()
    return files


def pack_in(list, filename):
    nfile = open(filename, "w")
    for item in list:
        str_item = ""
        l_item = len(item)
        for i in range(l_item - 1):
            str_item += item[i] + "|"
        str_item += item[l_item - 1]
        nfile.write(str_item + "\n")
    nfile.close()


def chr_increment(c):
    return chr(ord(c) + 1) if c != 'Z' else 'A'


def str_increment(s):
    lost_part = s.rstrip('Z')
    num_replacements = len(s) - len(lost_part)
    new_s = lost_part[:-1] + chr_increment(lost_part[-1]) if lost_part else 'A'
    new_s += 'A' * num_replacements
    return new_s


def weekday_translate(english):
    if english == "Mon":
        return "ponedeljak"
    if english == "Tue":
        return "utorak"
    if english == "Wed":
        return "sreda"
    if english == "Thu":
        return "cetvrtak"
    if english == "Fri":
        return "petak"
    if english == "Sat":
        return "subota"
    if english == "Sun":
        return "nedelja"


def generate_pt():
    today = datetime.today().date()
    projection_times_copy = projection_times.copy()

    whole_id = ""
    date_pt = ""

    # generisanje ove nedelje
    for i in range(7):
        todays_weekday_english = today.strftime("%a")
        todays_weekday_serbian = weekday_translate(todays_weekday_english)
        for projection in projections:
            if projection[1] != "x":
                projection_time = [whole_id, date_pt]
                id_second_part = "AA"
                if projection_times:
                    for projtime in projection_times:
                        if projtime[0][:4] == projection[0]:
                            id_second_part = str_increment(id_second_part)
                for weekday in projection[4].split(","):
                    if todays_weekday_serbian == weekday:

                        projection_time[0] = projection[0] + id_second_part
                        projection_time[1] = today.strftime("%d.%m.%Y.")
                        add = 1
                        for projtime in projection_times_copy:
                            formatedtime = datetime.strptime(projtime[1], "%d.%m.%Y.").date()
                            if formatedtime >= today:
                                add = 0
                        if add > 0:
                            id_second_part = str_increment(id_second_part)
                            projection_time[0] = projection[0] + id_second_part
                            projection_times.append(projection_time)
        today += timedelta(1)

    # generisanje druge nedelje
    for i in range(7):
        todays_weekday_english = today.strftime("%a")
        todays_weekday_serbian = weekday_translate(todays_weekday_english)
        for projection in projections:
            if projection[1] != "x":
                projection_time1 = [whole_id, date_pt]
                id_second_part = "AA"
                if projection_times:
                    for projtime in projection_times:
                        if projtime[0][:4] == projection[0]:
                            id_second_part = str_increment(id_second_part)
                for weekday in projection[4].split(","):
                    if todays_weekday_serbian == weekday:

                        projection_time1[0] = projection[0] + id_second_part
                        projection_time1[1] = today.strftime("%d.%m.%Y.")
                        add = 1
                        for projtime in projection_times_copy:
                            formatedtime = datetime.strptime(projtime[1], "%d.%m.%Y.").date()
                            if formatedtime >= today:
                                add = 0
                        if add > 0:
                            id_second_part = str_increment(id_second_part)
                            projection_time1[0] = projection[0] + id_second_part
                            projection_times.append(projection_time1)
        today += timedelta(1)


def projection_time_search():
    try:
        option = int(input("Pretraga termina bioskopskih projekcija:\n"
                           "1 - pretraga po filmu\n"
                           "2 - pretraga po sali\n"
                           "3 - pretraga po datumu odrzavanja\n"
                           "4 - pretraga po vremenu pocetka i kraja\n"
                           "0 - nazad\n"))
    except ValueError:
        print("Nevalidan unos\n")
        return
    found_p_times = []
    if option == 0:
        return
    elif option == 1:
        string = input("Unesite ime filma: ")
        for projection in projections:
            if string == projection[5]:
                for projection_time in projection_times:
                    if projection_time[0][:4] == projection[0]:
                        found_p_times.append(projection_time)
    elif option == 2:
        string = input("Unesite sifru sale: ")
        for projection in projections:
            if string == projection[1]:
                for projection_time in projection_times:
                    if projection_time[0][:4] == projection[0]:
                        found_p_times.append(projection_time)
    elif option == 3:
        string = input("Unesite datum u obliku DD.MM.YYYY. : ")
        for projection in projections:
            for projection_time in projection_times:
                if projection_time[0][:4] == projection[0]:
                    if projection_time[1] == string:
                        found_p_times.append(projection_time)
    elif option == 4:
        start = input("Unesite trazeni pocetak filma u formatu HH:MM : ")
        end = input("Unesite trazeni kraj filma u formatu HH:MM : ")
        for projection in projections:
            if start == projection[2] and end == projection[3]:
                for projection_time in projection_times:
                    if projection_time[0][:4] == projection[0]:
                        found_p_times.append(projection_time)
    if found_p_times:
        print("*" * 170)
        print(
            "|{0:30}|{1:6}|{2:15}|{3:10}|{4:10}|{5:6}|{6:10}\n".format("Naziv filma", "Sala: ", "Datum: ", "Pocetak: ",
                                                                       "Kraj: ", "Cena: ", "Sifra: "))
        for found_proj in found_p_times:
            for projection in projections:
                if found_proj[0][:4] == projection[0]:
                    print("|{0:30}|{1:6}|{2:15}|{3:10}|{4:10}|{5:6}|{6:10}\n".format(projection[5], projection[1],
                                                                                     found_proj[1], projection[2],
                                                                                     projection[3],
                                                                                     projection[6], found_proj[0]))
        print("*" * 170)
    else:
        print("Nema takvih projekcija\n")


def unique_test(idname, list):
    for i in range(len(list)):
        if idname == list[i][0]:
            return 0
    return 1


def unique_any_test(name, list, index):
    for i in range(len(list)):
        if idname == list[i][index]:
            return False
    return True


def password_test(password):
    if len(password) <= 6:
        return 0
    for i in password:
        if i.isnumeric():
            return 1
    return 0


def register(user_id, password, ime, prezime, uloga, list):
    userdata = [user_id, password, ime, prezime, uloga]
    list.append(userdata)


def password_matching(idname, password, list):
    index = -1
    for i in range(len(list)):
        if idname == list[i][0]:
            index = i
            break

    if password == list[index][1]:
        return 1
    return 0


def index_finder(id, list):
    index = -1
    for i in range(len(list)):
        if id == list[i][0]:
            index = i
    return index


def login(idname, list):
    print("Uspesno ste ulogovani kao " + idname + "\n")
    user = list[index_finder(idname, list)]
    if user[4] == "kupac":
        kupac_menu(user, list)
    elif user[4] == "prodavac":
        prodavac_menu(user, list)
    elif user[4] == "menadzer":
        menadzer_menu(user, list)


def display_all_films():
    # naziv,zanr,trajanje,reziser,glavni glumci,zemlja porekla, godina proizvodnje
    print("|{0:20}|{1:30}|{2:10}|{3:20}|{4:40}|{5:20}|{6:5}".format("Naziv filma:", "Zanr:", "Trajanje:", "Reziser:",
                                                                    "Glavni glumci:", "Zemlja porekla: ",
                                                                    "Godina proizvodnje:"))

    print("*" * 170)
    for film in films:
        print("|{0:20}|{1:30}|{2:10}|{3:20}|{4:40}|{5:20}|{6:5}".format(film[0], film[1], film[2], film[3], film[4],
                                                                        film[5], film[6]))
    print("*" * 170)


def simple_search(option, q_string, *args):
    # imamo 4 opcije:
    # bez pomocne liste pretragu
    # sa pomocnom listom gde je potrebam jedan podatak
    # sa pomocnom listom gde je potrebno vise podataka
    # sa potrebnom konverzijom u broj i proverom da li broj valja
    found_films = []
    called_from_multiple = 1
    if not args:
        called_from_multiple = 0

    if option == 1 or option == 6:
        for film in films:
            if film[option - 1] == q_string:
                found_films.append(film)
    elif option == 2:
        for film in films:
            parts = film[option - 1].split(",")
            for part in parts:
                if part == q_string:
                    found_films.append(film)
    elif option == 3:
        try:
            lengths = q_string.split(" ")
            min = int(lengths[0])
            max = int(lengths[1])
        except:
            print("Pogresan unos, trebali ste odvojiti tacno jednim razmakom dva broja")
            return
        for film in films:
            film_length = 0
            film_length = int(film[2])
            if min <= film_length <= max:
                found_films.append(film)
    elif option == 4 or option == 5:
        question_people = []
        question_people.append(q_string)
        more = 1
        while more > 0:
            man = input("Unesite sledeceg, a za kraj ukucajte x: ")
            if man == "" or man == "x" or man == "X":
                more = 0
            else:
                question_people.append(man)

        for film in films:
            people = film[option - 1].split(",")
            for human in people:
                for man in question_people:
                    if man == human:
                        if unique_test(film[0], found_films):
                            found_films.append(film)
    elif option == 7:
        try:
            q_year = int(q_string)
        except ValueError:
            print("Pogresan unos, morate uneti samo godinu bez tacke ili bilo cega drugog\n")
            return
        for film in films:
            year = int(film[6])
            if q_year == year:
                found_films.append(film)

    if not found_films:
        print("Nema pod ovim kriterijumima nijedan film\n")
    elif called_from_multiple == 1:
        return found_films
    else:
        print("*" * 170)
        print("|{0:20}|{1:30}|{2:10}|{3:20}|{4:40}|{5:20}|{6:5}".format("Naziv filma:", "Zanr:", "Trajanje:", "Reziser:",
                                                                        "Glavni glumci:", "Zemlja porekla: ",
                                                                        "Godina proizvodnje:"))
        for film in found_films:
            print("|{0:20}|{1:30}|{2:10}|{3:20}|{4:40}|{5:20}|{6:5}".format(film[0], film[1], film[2], film[3], film[4],
                                                                            film[5], film[6]))
        print("*" * 170)


def multiple_choice_merge(list1, list2):
    final = []
    if list1 and list2:
        for i in list1:
            for j in list2:
                if i[0] == j[0]:
                    final.append(i)
                    break
        return final

    return []


def multiple_choice_search():
    # algoritam ide tako da nadjem filmove po jednom parametru, pa po drugom, pa spojim
    multiple_found = []
    found_films_1 = []
    found_films_2 = []
    print("NAPOMENA: ne morate uneti sve podatke, unesite enter ako neki ne zelite")

    question_string = input("Unesite naziv filma: ")
    first = 1
    if question_string != "":
        first = 0
        found_films_1 = simple_search(1, question_string, 1)
        multiple_found = found_films_1

    question_string = input("Unesite zanr filma: ")
    if question_string != "":
        if first == 0:
            found_films_2 = simple_search(2, question_string, 1)
            multiple_found = multiple_choice_merge(found_films_1, found_films_2)
            found_films_1 = multiple_found
        else:
            found_films_1 = simple_search(2, question_string, 1)
            multiple_found = found_films_1
        first = 0

    question_string = input("Unesite minimalno pa maksimalno trajanje filma u minutima razdvojene jednim razmakom: ")
    if question_string != "":
        if first == 0:
            found_films_2 = simple_search(3, question_string, 1)
            multiple_found = multiple_choice_merge(found_films_1, found_films_2)
            found_films_1 = multiple_found
        else:
            found_films_1 = simple_search(3, question_string, 1)
            multiple_found = found_films_1
        first = 0

    question_string = input("Unesite rezisera filma: ")
    if question_string != "":
        if first == 0:
            found_films_2 = simple_search(4, question_string, 1)
            multiple_found = multiple_choice_merge(found_films_1, found_films_2)
            found_films_1 = multiple_found
        else:
            found_films_1 = simple_search(4, question_string, 1)
            multiple_found = found_films_1
        first = 0

    question_string = input("Unesite prvog glumca: ")
    if question_string != "":
        if first == 0:
            found_films_2 = simple_search(5, question_string, 1)
            multiple_found = multiple_choice_merge(found_films_1, found_films_2)
            found_films_1 = multiple_found
        else:
            found_films_1 = simple_search(5, question_string, 1)
            multiple_found = found_films_1
        first = 0

    question_string = input("Unesite zemlju porekla: ")
    if question_string != "":
        if first == 0:
            found_films_2 = simple_search(6, question_string, 1)
            multiple_found = multiple_choice_merge(found_films_1, found_films_2)
            found_films_1 = multiple_found
        else:
            found_films_1 = simple_search(6, question_string, 1)
            multiple_found = found_films_1
        first = 0

    question_string = input("Unesite godinu proizvodnje: ")
    if question_string != "":
        if first == 0:
            found_films_2 = simple_search(7, question_string, 1)
            multiple_found = multiple_choice_merge(found_films_1, found_films_2)
            found_films_1 = multiple_found
        else:
            found_films_1 = simple_search(7, question_string, 1)
            multiple_found = found_films_1
        first = 0

    if not multiple_found:
        print("Nema pod ovim kriterijumima nijedan film\n")
    else:
        print("*" * 170)
        print("|{0:20}|{1:30}|{2:10}|{3:20}|{4:40}|{5:20}|{6:5}".format("Naziv filma:", "Zanr:", "Trajanje:", "Reziser:",
                                                                        "Glavni glumci:", "Zemlja porekla: ",
                                                                        "Godina proizvodnje:"))
        for film in multiple_found:
            print("|{0:20}|{1:30}|{2:10}|{3:20}|{4:40}|{5:20}|{6:5}".format(film[0], film[1], film[2], film[3], film[4],
                                                                            film[5], film[6]))
        print("*" * 170)


def film_search():
    correct = 0
    while correct == 0:
        try:
            option = int(input("Pretrage filmova:\n"
                               "1 - Po nazivu\n"
                               "2 - Po zanru\n"
                               "3 - Po trajanju\n"
                               "4 - Po reziseru\n"
                               "5 - Po glavnim glumcima\n"
                               "6 - Po zemlji porekla\n"
                               "7 - Po godini proizvodnje\n"
                               "8 - Visekriterijumska pretraga\n"
                               "0 - nazad\n"))
        except ValueError:
            print("POGRESAN UNOS, POKUSAJTE PONOVO: \n")
            correct = 0
            continue
        if 0 <= option <= 8:
            correct = 1
        else:
            print("POGRESAN UNOS, MORA BITI IZMEDJU 0 I 8, POKUSAJTE PONOVO: \n")
    if option == 0:
        return
    elif option == 1:
        question_string = input("Unesite naziv filma: ")
        simple_search(1, question_string)
    elif option == 2:
        question_string = input("Unesite zanr filma: ")
        simple_search(2, question_string)
    elif option == 3:
        question_string = input(
            "Unesite minimalno pa maksimalno trajanje filma u minutima razdvojene jednim razmakom: ")
        simple_search(3, question_string)
    elif option == 4:
        question_string = input("Unesite prvog rezisera filma: ")
        simple_search(4, question_string)
    elif option == 5:
        question_string = input("Unesite prvog glumca: ")
        simple_search(5, question_string)
    elif option == 6:
        question_string = input("Unesite zemlju porekla: ")
        simple_search(6, question_string)
    elif option == 7:
        question_string = input("Unesite godinu proizvodnje: ")
        simple_search(7, question_string)
    elif option == 8:
        multiple_choice_search()


def display_matrix_seats(*args):
    if not args:
        projection_time_id_exist = 1
        projection_time_id = input("Unesite sifru trazene projekcije: ")
    else:
        projection_time_id_exist = 1
        projection_time_id = args[0]

    if unique_test(projection_time_id, projection_times) > 0:
        projection_time_id_exist = 0
    if projection_time_id_exist > 0:
        projection_id = projection_time_id[:4]
        projection_index = index_finder(projection_id, projections)
        hall_id = projections[projection_index][1]
        hall_index = index_finder(hall_id, halls)
        seat_columns = halls[hall_index][3].split(",")
        seat_rows = []
        for i in range(int(halls[hall_index][2])):
            seat_rows.append(i + 1)
        matrix = []
        for row in seat_rows:
            m_row = []
            for column in seat_columns:
                m_row.append(1)
            matrix.append(m_row)
        # ovako je kad je sve slobodno
        # ovde treba proveriti da li je zapravo...
        for ticket in tickets:
            if ticket[3] == projection_time_id and ticket[4] != "x":
                t_seat = ticket[4].split()
                t_row = int(t_seat[0])
                t_column = t_seat[1]
                t_row -= 1
                t_column = ord(t_column)
                t_column -= ord('A')
                matrix[t_row][t_column] = 0

        for row in seat_rows:
            print("{0:2}: ".format(row), end="")
            for column in seat_columns:
                if matrix[seat_rows.index(row)][seat_columns.index(column)] > 0:
                    print("{0:4}".format(column), end="")
                else:
                    print("x   ", end="")
            print("\n")
    else:
        print("Nepostojeca projekcija \n")


def seat_exist(proj_time_id, seat_id):
    qseat = seat_id.split()
    try:
        qrow = int(qseat[0])
        qrow -= 1
        qcolumn = ord(qseat[1]) - ord('A')
    except:
        return 0

    if qseat == "" or qrow == None or qcolumn == None or qrow < 0 or qcolumn < 0:
        return 0
    projection_id = proj_time_id[:4]
    projection_index = index_finder(projection_id, projections)
    hall_id = projections[projection_index][1]
    hall_index = index_finder(hall_id, halls)
    seat_columns = halls[hall_index][3].split(",")
    seat_rows = []
    for i in range(int(halls[hall_index][2])):
        seat_rows.append(i + 1)
    candidate = 0
    for column in seat_columns:
        if ord(column) - ord('A') == qcolumn:
            candidate = 1
            break
    if candidate == 0:
        return 0
    for row in seat_rows:
        if row == qrow + 1:
            return 1
    return 0


def seat_free(proj_time_id, seat_id):
    if seat_exist(proj_time_id, seat_id) == 0:
        return 0
    projection_id = proj_time_id[:4]
    projection_index = index_finder(projection_id, projections)
    hall_id = projections[projection_index][1]
    hall_index = index_finder(hall_id, halls)
    seat_columns = halls[hall_index][3].split(",")
    seat_rows = []
    for i in range(int(halls[hall_index][2])):
        seat_rows.append(i + 1)
    matrix = []
    for row in seat_rows:
        m_row = []
        for column in seat_columns:
            m_row.append(1)
        matrix.append(m_row)
    # ovako je kad je sve slobodno
    # ovde treba proveriti da li je zapravo...
    for ticket in tickets:
        if ticket[3] == proj_time_id and ticket[4] != "x":
            t_seat = ticket[4].split()
            t_row = int(t_seat[0])
            t_column = t_seat[1]
            t_row -= 1
            t_column = ord(t_column)
            t_column -= ord('A')
            matrix[t_row][t_column] = 0
    # 0 - zauzeto
    # 1 - slobodno
    qseat = seat_id.split()
    qrow = int(qseat[0])
    qrow -= 1
    qcolumn = ord(qseat[1]) - ord('A')
    return matrix[qrow][qcolumn]


def ticket_reservation(user):
    # biranje projekcije
    # za tiket nam treba redom:
    # id, Ime i prezime, userid, termin projekcije, oznaka sedista, datum prodaje, rez/kupljena -> 0/1
    while True:
        correct = 0
        while correct == 0:
            try:
                correct = 1
                option = int(input("1 - unesi sifru projekcije\n"
                                   "2 - pretrazi projekcije\n"
                                   "0 - nazad\n"))
            except ValueError:
                print("Pogresan unos, probajte ponovo:\n")
                correct = 0

        if option == 0:
            return
        elif option == 1:
            projection_code = input("Sifra projekcije: ")
            i = index_finder(projection_code,projection_times)
            if i != -1:
                print("Prikaz sedista za ovu projekciju: \n")
                display_matrix_seats(projection_code)
            else:
                print("Pogresna sifra!\n")
                break
            if user[4] == "kupac":
                user_id = user[0]
                whole_name = user[2] + " " + user[3]
            elif user[4] == "prodavac":
                while True:
                    try:
                        opt2 = int(input("1 - registrovan kupac\n"
                                         "2 - neregistrovan kupac\n"))
                        if opt2 > 2 or 0 > opt2:
                            print("Probaj ponovo, 1 ili 2 \n")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Pogresan unos, 1 ili 2 treba...\n")
                if opt2 == 1:
                    user_id = input("Unesite username kupca: ")
                    i = index_finder(user_id, users)
                    if i == -1:
                        print("Neispravan username...\n")
                        continue
                    whole_name = users[i][2] + " " + users[i][3]
                elif opt2 == 2:
                    user_id = "None"
                    while True:
                        whole_name = input("Unesite ime i prezime kupca: ")
                        if whole_name != "":
                            break
            while True:
                seat_id = input("Unesite oznaku sedista, red pa kolona, odvojeni jednim razmakom (npr 7 A): ")
                if seat_exist(projection_code, seat_id) > 0 and seat_free(projection_code, seat_id) > 0:
                    break
                elif seat_exist(projection_code, seat_id) == 0:
                    print("Nepostojece sediste ili nevaljana oznaka sedista\n")
                    continue
                elif seat_free(projection_code, seat_id) == 0:
                    print("Zauzeto sediste\n")
                    continue
            today = datetime.today().date()
            date_reserved = today.strftime("%d.%m.%Y.")
            id = 0
            for ticket in tickets:
                id += 1
            id = str(id)
            tickets.append([id, whole_name, user_id, projection_code, seat_id, date_reserved, "0"])
            print("Karta je uspesno rezervisana!\n")
        elif option == 2:
            projection_time_search()


def display_all_tickets():
    # oznaku termina bioskopske projekcije, ime i prezime kupca, naziv filma, datum, vreme početka
    # i vreme kraja filma, sedište(eventualno još neke informacije koje smatrate relevantnim),
    # podatak da li je upitanju prodata ili rezervisana karta.
    print("*" * 150)
    print("{0:14}|{1:30}|{2:30}|{3:15}|{4:10}|{5:8}|{6:10}|{7:10}|{8:8}\n".format("Projekcija: ", "Kupac: ", "Film: ",
                                                                                  "Datum: ", "Pocetak: ",
                                                                                  "Kraj: ", "Sediste: ", "Prodata: ",
                                                                                  "Sifra karte:"))
    for ticket in tickets:
        if ticket[4] != "x":
            projection_id = ticket[3][:4]
            projection_index = index_finder(projection_id, projections)
            film_name = projections[projection_index][5]
            film_start = projections[projection_index][2]
            film_end = projections[projection_index][3]
            projection_time_index = index_finder(ticket[3], projection_times)
            film_date = projection_times[projection_time_index][1]
            if ticket[6] == "0":
                prodata = "Ne"
            else:
                prodata = "Da"
            print("{0:14}|{1:30}|{2:30}|{3:15}|{4:10}|{5:8}|{6:10}|{7:10}|{8:8}\n".format(ticket[3], ticket[1], film_name,
                                                                                         film_date,
                                                                                         film_start, film_end, ticket[4],
                                                                                         prodata, ticket[0]))
    print("*" * 150)


def display_my_tickets(user):
    print("*" * 150)
    print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format("Projekcija: ", "Film: ",
                                                                           "Datum: ", "Pocetak: ",
                                                                           "Kraj: ", "Sediste: ", "Prodata: ",
                                                                           "Sifra karte: "))
    for ticket in tickets:
        if ticket[2] == user[0] and ticket[4] != "x":
            projection_id = ticket[3][:4]
            projection_index = index_finder(projection_id, projections)
            film_name = projections[projection_index][5]
            film_start = projections[projection_index][2]
            film_end = projections[projection_index][3]
            projection_time_index = index_finder(ticket[3], projection_times)
            film_date = projection_times[projection_time_index][1]
            if ticket[6] == "0":
                prodata = "Ne"
            else:
                prodata = "Da"
            print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(ticket[3], film_name,
                                                                                   film_date,
                                                                                   film_start, film_end, ticket[4],
                                                                                   prodata, ticket[0]))
    print("*" * 150)


def display_one_ticket(ticket):
    projection_id = ticket[3][:4]
    projection_index = index_finder(projection_id, projections)
    film_name = projections[projection_index][5]
    film_start = projections[projection_index][2]
    film_end = projections[projection_index][3]
    projection_time_index = index_finder(ticket[3], projection_times)
    film_date = projection_times[projection_time_index][1]
    if ticket[6] == "0":
        prodata = "Ne"
    else:
        prodata = "Da"
    print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(ticket[3], film_name,
                                                                           film_date,
                                                                           film_start, film_end, ticket[4],
                                                                           prodata, ticket[0]))


def ticket_delete(*args):
    if not args:
        ticket_id = input("Unesite sifru karte koju zelite obrisati: ")
        if index_finder(ticket_id, tickets) == -1:
            print("Nepostojeca karta...\n")
            return
        cancel_delete = input("Da li ste sigurni? Ukucajte x za odustajanje, a enter za nastavak: ")
        if cancel_delete == "x":
            return
    if args:
        ticket_id = args[0]

    ticket_id = int(ticket_id)
    tickets[ticket_id][1] = "Ponistena karta"
    tickets[ticket_id][2] = "Ponistena"
    tickets[ticket_id][4] = "x"
    # id ostavljamo kakav je i bio, arhivirana je karta takoreci


def ticket_search():
    try:
        option = int(input("Izaberite kriterijum pretrage:\n"
                           "1 - sifra projekcije\n"
                           "2 - datum projekcije\n"
                           "3 - vreme pocetka\n"
                           "4 - vreme kraja\n"
                           "5 - prikaz svih rezervisanih \n"
                           "6 - prikaz svih kupljenih\n"))
    except ValueError:
        print("Pogresan unos, unos mora biti izmedju 0 i 6\n")
        return
    if option == 1:
        proj_id = input("Unesite sifru projekcije: ")
        found = 0
        for ticket in tickets:
            if proj_id == ticket[3] and ticket[4] != "x":
                found += 1
                if found == 1:
                    print("*" * 150)
                    print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format("Projekcija: ", "Film: ",
                                                                                           "Datum: ", "Pocetak: ",
                                                                                           "Kraj: ", "Sediste: ",
                                                                                           "Prodata: ",
                                                                                           "Sifra karte: "))
                display_one_ticket(ticket)
        if found > 0:
            print("*" * 150)
        else:
            print("Nema karata koje odgovaraju kriterijumu.\n")
    elif option == 2:
        q_date = input("Unesite datum u formatu DD.MM.YYYY. : ")
        found = 0
        for ticket in tickets:
            for projection_time in projection_times:
                if ticket[3] == projection_time[0]:
                    if q_date == projection_time[1] and ticket[4] != "x":
                        found += 1
                        if found == 1:
                            print("*" * 150)
                            print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(
                                "Projekcija: ", "Film: ", "Datum: ", "Pocetak: ",
                                "Kraj: ", "Sediste: ", "Prodata: ", "Sifra karte: "))
                        display_one_ticket(ticket)
        if found > 0:
            print("*" * 150)
        else:
            print("Nema karata koje odgovaraju kriterijumu.\n")
    elif option == 3 or option == 4:
        q_time = input("Unesite vreme u formatu HH:MM : ")
        found = 0
        for ticket in tickets:
            q_projection_id = ticket[3][:4]
            for projection in projections:
                if q_projection_id == projection[0]:
                    if q_time == projection[2] and option == 3 and ticket[4] != "x":
                        found += 1
                        if found == 1:
                            print("*" * 150)
                            print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(
                                "Projekcija: ", "Film: ", "Datum: ", "Pocetak: ", "Kraj: ", "Sediste: ", "Prodata: ",
                                "Sifra karte: "))
                        display_one_ticket(ticket)
                    if q_time == projection[3] and option == 4 and ticket[4] != "x":
                        found += 1
                        if found == 1:
                            print("*" * 150)
                            print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(
                                "Projekcija: ", "Film: ", "Datum: ", "Pocetak: ", "Kraj: ", "Sediste: ", "Prodata: ",
                                "Sifra karte: "))
                        display_one_ticket(ticket)
        if found > 0:
            print("*" * 150)
        else:
            print("Nema karata koje odgovaraju kriterijumu.\n")
    elif option == 5 or option == 6:
        display_bought = option - 5
        if display_bought > 0:
            found = 0
            for ticket in tickets:
                if ticket[6] == "1" and ticket[4] != "x":
                    found += 1
                    if found == 1:
                        print("*" * 150)
                        print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(
                            "Projekcija: ", "Film: ", "Datum: ", "Pocetak: ", "Kraj: ", "Sediste: ", "Prodata: ",
                            "Sifra karte: "))
                    display_one_ticket(ticket)
            if found > 0:
                print("*" * 150)
            else:
                print("Nema karata koje odgovaraju kriterijumu.\n")
        else:
            found = 0
            for ticket in tickets:
                if ticket[6] == "0" and ticket[4] != "x":
                    found += 1
                    if found == 1:
                        print("*" * 150)
                        print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(
                            "Projekcija: ", "Film: ", "Datum: ", "Pocetak: ", "Kraj: ", "Sediste: ", "Prodata: ",
                            "Sifra karte: "))
                    display_one_ticket(ticket)
            if found > 0:
                print("*" * 150)
            else:
                print("Nema karata koje odgovaraju kriterijumu.\n")


def create_loyalty_card():
    while True:
        user_id = input("Unesite username kupca kom izradjujete: ")
        if unique_test(user_id,users) == 0:
            break
    # 1 - izvucemo sve PRODATE karte ovom useru
    # 2 - pazimo da je datum noviji od 30 dana pre danasnjeg

    my_tickets = []
    for ticket in tickets:
        if user_id == ticket[2] and ticket[6] == "1":
            # kvalifikovana karta
            today = datetime.today()
            i = index_finder(ticket[3],projection_times)
            ticket_time_str = projection_times[i][1]
            ticket_time = datetime.strptime(ticket_time_str, "%d.%m.%Y.")
            if today - ticket_time < timedelta(days=365):
                my_tickets.append(ticket)
    sum = 0
    for ticket in my_tickets:
        for sale in sales:
            if ticket[0] == sale[0]:
                sum += int(sale[1])

    if sum >= 5000:
        print("Korisnik "+ user_id + " ima pravo na kartu lojalnosti! \n")
        today_str = today.strftime("%d.%m.%Y.")
        new_card = [user_id, today_str]
        loyalty_cards.append(new_card)
    else:
        missing = 5000 - sum
        print("Korisniku "+user_id+" fali jos " + str(missing) + " potrosenih dinara ovog meseca da bi mogao izraditi karticu lojalnosti.\n")


def price_adjustment(price, proj_time_id, buyer_id, proj_id):
    # 1. provera dana u nedelji
    proj_time_index = index_finder(proj_time_id,projection_times)
    date_string = projection_times[proj_time_index][1]
    date = datetime.strptime(date_string, "%d.%m.%Y.")
    day = date.weekday()
    if day == 1:
        price = price - 50
    elif day == 5 or day == 6:
        price = price + 50

    # 2. provera kartice lojalnosti
    if index_finder(buyer_id, loyalty_cards) == -1:
        return price
    else:
        loyalty_card_index = index_finder(buyer_id, loyalty_cards)
        loyal_from_date = datetime.strptime(loyalty_cards[loyalty_card_index][1], "%d.%m.%Y.")
        if loyal_from_date <= date:
            price = price * 0.9
        return price


def ticket_selling(salesman_id):
    # za prodaju treba nam redom:
    # ticket_id, cena, id_prodavca, datum_prodaje
    ticket_id = input("Unesite sifru karte koju prodajete: ")
    ticket_index = index_finder(ticket_id, tickets)
    proj_index = index_finder(tickets[ticket_index][3][:4], projections)

    if ticket_index == -1:
        print("Nepostojeca karta\n")
    elif tickets[ticket_index][4] == "x":
        print("Ponistena karta, nemoguce\n")
    elif tickets[ticket_index][6] == "1":
        print("Karta je vec prodata!\n")
    else:
        price = int(projections[proj_index][6])
        tickets[ticket_index][6] = "1"
        print("Prodata karta sifre " + ticket_id + "\n")

        date_string = datetime.now().strftime("%d.%m.%Y.")
        tickets[ticket_index][5] = date_string
        price = price_adjustment(price, tickets[ticket_index][3] , tickets[ticket_index][2], tickets[ticket_index][3][:4])
        this_sale = [ticket_id, str(price), salesman_id, date_string]
        sales.append(this_sale)


def direct_ticket_sell(salesman_id):
    # za tiket nam treba redom:
    # id, Ime i prezime, userid, termin projekcije, oznaka sedista, datum prodaje, KUPLJENA = 1

    # za prodaju treba nam redom:
    # ticket_id, cena, id_prodavca, datum_prodaje

    while True:
        correct = 0
        while correct == 0:
            try:
                correct = 1
                option = int(input("1 - unesi sifru projekcije\n"
                                   "2 - pretrazi projekcije\n"
                                   "0 - nazad\n"))
            except ValueError:
                print("Pogresan unos, probajte ponovo:\n")
                correct = 0

        if option == 0:
            return
        elif option == 1:
            while True:
                projection_code = input("Sifra projekcije: ")
                i = -1
                for projection_time in projection_times:
                    if projection_time[0] == projection_code:
                        i = index_finder(projection_time[0], projection_times)
                        break
                if i != -1:
                    print("Prikaz sedista za ovu projekciju: \n")
                    display_matrix_seats(projection_code)
                    break
                else:
                    print("Greska!\n")
            while True:
                try:
                    opt2 = int(input("1 - registrovan kupac\n"
                                     "2 - neregistrovan kupac\n"))
                    if opt2 > 2 or 0 > opt2:
                        print("Probaj ponovo, 1 ili 2 \n")
                        continue
                    else:
                        break
                except ValueError:
                    print("Pogresan unos, 1 ili 2 treba...\n")
            if opt2 == 1:
                user_id = input("Unesite username kupca: ")
                i = index_finder(user_id, users)
                if i == -1:
                    print("Neispravan username...\n")
                    continue
                whole_name = users[i][2] + " " + users[i][3]
            elif opt2 == 2:
                user_id = "None"
                while True:
                    whole_name = input("Unesite ime i prezime kupca: ")
                    if whole_name != "":
                        break
            while True:
                seat_id = input("Unesite oznaku sedista, red pa kolona, odvojeni jednim razmakom (npr 7 A): ")
                if seat_exist(projection_code, seat_id) > 0 and seat_free(projection_code, seat_id) > 0:
                    break
                elif seat_exist(projection_code, seat_id) == 0:
                    print("Nepostojece sediste ili nevaljana oznaka sedista\n")
                    continue
                elif seat_free(projection_code, seat_id) == 0:
                    print("Zauzeto sediste\n")
                    continue
            today = datetime.today().date()
            date_reserved = today.strftime("%d.%m.%Y.")
            id = 0
            for ticket in tickets:
                id += 1
            id = str(id)
            tickets.append([id, whole_name, user_id, projection_code, seat_id, date_reserved, "1"])
            print("Karta je uspesno kupljena!\n")

            proj_index = index_finder(projection_code[:4], projections)
            price = int(projections[proj_index][6])

            date_string = datetime.now().strftime("%d.%m.%Y.")
            price = price_adjustment(price, tickets[int(id)][3], tickets[int(id)][2], tickets[int(id)][3][:4])
            this_sale = [id, str(price), salesman_id, date_string]
            sales.append(this_sale)

        elif option == 2:
            projection_time_search()


def ticket_change():
    while True:
        projection_time_id = input("Unesite sifru projekcije: ")
        projection_time_index = index_finder(projection_time_id, projection_times)
        if projection_time_index != -1:
            break
        print("Nepostojeca projekcija\n")
    fullname = input("Unesite ime i prezime kupca odvojeno tacno jednim razmakom: ")
    while True:
        seat_number = input("Unesite oznaku sedista (npr. 7 A): ")
        if seat_exist(projection_time_id, seat_number):
            break
        print("Nepostojece sediste\n")
    not_found = True
    for ticket in tickets:
        if ticket[1] == fullname and ticket[3] == projection_time_id and ticket[4] == seat_number:
            not_found = False
            while True:
                try:
                    option = int(input("1 - izmena termina projekcije\n"
                                       "2 - izmena imena i prezimena kupca\n"
                                       "3 - izmena sedista u sali\n"
                                       "0 - nazad\n"))
                    break
                except ValueError:
                    print("Pogresan unos\n")
            if option == 0:
                return
            elif option == 1:
                while True:
                    projection_time_id1 = input("Unesite novu sifru projekcije: ")
                    projection_time_index = index_finder(projection_time_id1, projection_times)
                    if projection_time_index != -1:
                        break
                    print("Nepostojeca projekcija\n")
                ticket[3] = projection_time_id1
            elif option == 2:
                while True:
                    fullname1 = input("Unesite novo ime i prezime kupca odvojeno tacno jednim razmakom: ")
                    try:
                        if fullname1.split()[0] and fullname1.split()[1]:
                            ticket[1] = fullname1
                            break
                    except IndexError:
                        print("Pogresan unos\n")
            elif option == 3:
                display_matrix_seats(projection_time_id)
                while True:
                    seat_number1 = input("Unesite oznaku sedista (npr. 7 A): ")
                    if seat_free(projection_time_id, seat_number1):
                        ticket[4] = seat_number1
                        break
                    elif seat_exist(projection_time_id, seat_number1):
                        print("Sediste je zauzeto.\n")
                    else:
                        print("Nepostojece sediste\n")
    if not_found:
        print("Nepostojeca karta!\n")

def automatic_delete_reservations():
    delete_time = datetime.today()
    for ticket in tickets:
        if ticket[6] == "0":
            for projection_time in projection_times:
                if projection_time[0] == ticket[3] and projection_time[1] == datetime.today().strftime("%d.%m.%Y."):
                    for projection in projections:
                        if projection[0] == projection_time[0][:4]:
                            date_time_str = projection_time[1] + " " + projection[2]
                            date_time_proj = datetime.strptime(date_time_str, "%d.%m.%Y. %H:%M")
                            if timedelta(minutes=30) > delete_time - date_time_proj:
                                ticket_delete(ticket[0])


def valid_ticket_for_user_delete(user_id, ticket_id):
    if index_finder(ticket_id, tickets) != -1:
        if tickets[int(ticket_id)][2] == user_id and tickets[int(ticket_id)][6] == "0":
            return True
        elif tickets[int(ticket_id)][6] == "1":
            print("Vec prodata karta\n")
            return False
    print("Nevalidna sifra.\n")
    return False


def repertoire_change():
    while True:
        try:
            option = int(input("1 - dodavanje filma\n"
                               "2 - izmena postojeceg filma\n"
                               "3 - brisanje postojeceg filma\n"
                               "0 - nazad\n"))
            if option > 3 or option < 0:
                print("Pogresan unos\n")
                continue
        except ValueError:
            print("Pogresan unos\n")
            continue
        if option == 0:
            return
        elif option == 1 or option == 2:
            # naziv,zanr,trajanje,reziser,glavni glumci,zemlja porekla, godina proizvodnje
            if option == 2:
                film_name = input("Unesite staro ime filma: ")
                if unique_test(film_name, films) == 0 and film_name != "":
                    index_film = index_finder(film_name, films)
                    print("Odabrani film:\n")
                    i = index_film
                    print("|{0}|{1}|{2}|{3}|{4}|{5}|{6}|\n".
                          format(films[i][0], films[i][1], films[i][2], films[i][3], films[i][4], films[i][5],
                                 films[i][6]))
                elif film_name == "":
                    print("Ne mozete ostaviti ovo polje prazno.\n")
                else:
                    print("Nepostojeci film.\n")

            while True:
                film_name = input("Unesite novo ime filma: ")
                if unique_test(film_name, films) > 0 and film_name != "":
                    break
                elif film_name == "":
                    print("Ne mozete ostaviti ovo polje prazno.\n")
                elif option == 2:
                    break
                else:
                    print("Postojeci film.\n")
            while True:
                film_genres = []
                no_genre = False
                number_of_genres = 0
                film_genre = input("Unesite zanr filma sa velikim pocetnim slovom\n")
                if film_genre == "":
                    print("Morate napisati bar jedan ili da je Nepoznato\n")
                    continue
                elif film_genre == "Nepoznato":
                    film_genres.append(film_genre)
                    no_genre = True
                else:
                    if film_genre.istitle():
                        film_genres.append(film_genre)
                        number_of_genres += 1
                    else:
                        print("Mora poceti VELIKIM slovom\n")
                        continue
                if not no_genre:
                    while True:
                        film_genre = input("Unesite sledeci zanr ili x za kraj: ")
                        if (film_genre == "" or not film_genre.istitle()) and film_genre != "x":
                            print("Nevalidan unos\n")
                            continue
                        elif film_genre == "x" or film_genre == "X":
                            break
                        else:
                            film_genres.append(film_genre)
                            number_of_genres += 1

                films_genres_str = ""
                i = 1
                for genre in film_genres:
                    films_genres_str += genre
                    if i < number_of_genres:
                        films_genres_str += ","
                    i += 1
                break

            while True:
                try:
                    film_duration = int(input("Unesite trajanje novog filma u minutama: "))
                    if film_duration > 1000 or film_duration < 1:
                        print("Duzina je u minutama i mora biti izmedju 1 i 1000\n")
                        continue
                    else:
                        break
                except ValueError:
                    print("Pogresan unos\n")
            while True:
                film_directors = []
                number_of_directors = 0
                film_director = input("Unesite rezisera filma: ")
                if film_director != "":
                    film_directors.append(film_director)
                    number_of_directors += 1
                else:
                    print("Ne mozete ostaviti ovo polje prazno\n")
                    continue
                while True:
                    film_director = input("Unesite sledeceg rezisera ili x za kraj: ")
                    if film_director != "" and film_director != "x" and film_director != "X":
                        film_directors.append(film_director)
                        number_of_directors += 1
                    elif film_director == "x" or film_director == "X":
                        break
                    else:
                        print("Pogresan unos\n")
                film_directors_str = ""
                i = 1
                for director in film_directors:
                    film_directors_str += director
                    if i < number_of_directors:
                        film_directors_str += ","
                    i += 1
                break
            while True:
                film_actors = []
                number_of_actors = 0
                film_actor = input("Unesite glavnog glumca filma: ")
                if film_actor != "":
                    film_actors.append(film_actor)
                    number_of_actors += 1
                else:
                    print("Ne mozete ostaviti ovo polje prazno\n")
                    continue
                while True:
                    film_actor = input("Unesite sledeceg glumca ili x za kraj: ")
                    if film_actor != "" and film_actor != "x" and film_actor != "X":
                        film_actors.append(film_actor)
                        number_of_actors += 1
                    elif film_actor == "x" or film_actor == "X":
                        break
                    else:
                        print("Pogresan unos\n")
                film_actors_str = ""
                i = 1
                for actor in film_actors:
                    film_actors_str += actor
                    if i < number_of_actors:
                        film_actors_str += ","
                    i += 1
                break

            while True:
                film_country = input("Unesite zemlju porekla filma: ")
                if film_country == "":
                    print("Ne moze biti prazno.\n")
                    continue
                else:
                    break
            while True:
                try:
                    film_year = int(input("Unesite godinu proizvodnje: "))
                    if film_year > 2024 or film_year < 1890:
                        print("Nevalidna godina proizvodnja, mora biti izmedju 1890 i 2024\n")
                        continue
                    break
                except ValueError:
                    print("Samo broj bez iceg, greska\n")
            # naziv,zanr,trajanje,reziser,glavni glumci,zemlja porekla, godina proizvodnje
            film = [film_name, films_genres_str, str(film_duration), film_directors_str, film_actors_str, film_country,
                    str(film_year)]
            if option == 1:
                films.append(film)
            elif option == 2:
                films[index_film] = film
        elif option == 3:
            film_name = input("Unesite ime filma: ")
            if unique_test(film_name, films) == 0 and film_name != "":
                index_film = index_finder(film_name, films)
                print("Odabrani film:\n")
                i = index_film
                print("|{0}|{1}|{2}|{3}|{4}|{5}|{6}|\n".
                      format(films[i][0], films[i][1], films[i][2], films[i][3], films[i][4], films[i][5], films[i][6]))
            elif film_name == "":
                print("Ne mozete ostaviti ovo polje prazno.\n")
            else:
                print("Nepostojeci film.\n")
            confirmation = input("Da li ste sigurni? Ukucajte x za odustanak, enter za nastavak: ")
            if confirmation == "x" or confirmation == "X":
                return
            else:
                del films[index_film]


def display_projections():
    print("Projekcije:\n")
    print("*"*150)
    for p in projections:
        if p[1] != "x":
            print("{0:6}|{1:4}|{2:8}|{3:8}|{4:30}|{5:30}|{6:7}\n".format(p[0], p[1], p[2], p[3], p[4], p[5], p[6]))
    print("*"*150)


def delete_reserved_for(projection_id):
    for ticket in tickets:
        if ticket[3][:4] == projection_id and ticket[6] == "0":
            ticket_delete(ticket[0])


def delete_next_2w_pt():
    global projection_times
    today = datetime.today()
    for proj_time in projection_times:
        proj_date = datetime.strptime(proj_time[1], "%d.%m.%Y.")
        pt_copy = proj_time
        if today - timedelta(days=1) <= proj_date:
            break

    projection_times_copy = projection_times.copy()
    i = index_finder(pt_copy[0], projection_times_copy)

    projection_times = projection_times[:i]


def projection_change():
    try:
        option = int(input("1 - dodaj novu projekciju\n"
                           "2 - izmeni postojecu projekciju\n"
                           "3 - obrisi postojecu projekciju\n"
                           "0 - nazad\n"))
        if 0 > option or 3 < option:
            print("Unos mora biti od 0 do 3\n")
            return
    except ValueError:
        print("Los unos\n")
        return
    if option == 0:
        return
    elif option == 1:
        # sifra, sala, vreme pocetka, vreme kraja, dani prikazivanja, naziv filma, cena
        display_projections()

        id_projection = 1111
        for proj in projections:
            id_projection += 1
        while True:
            hall = input("Unesite sifru sale: ")
            if unique_test(hall, halls) == 0:
                break
            else:
                print("Nepostojeca sala\n")
        while True:
            time_start = input("Unesite vreme pocetka u formatu HH:MM: ")
            try:
                hours = int(time_start.split(":")[0])
                minutes = int(time_start.split(":")[1])
                if hours < 0 or hours > 24 or minutes > 59 or minutes < 0:
                    print("Pogresan unos\n")
                    continue
                else:
                    break
            except:
                print("Pogresan unos\n")
                continue
        while True:
            time_end = input("Unesite vreme kraja u formatu HH:MM: ")
            try:
                hours = int(time_end.split(":")[0])
                minutes = int(time_end.split(":")[1])
                if hours < 0 or hours > 24 or minutes > 59 or minutes < 0:
                    print("Pogresan unos\n")
                    continue
                else:
                    break
            except:
                print("Pogresan unos\n")
                continue
        while True:
            weekdays = []
            try:
                first_time = True
                while True:
                    weekday = int(input("Unesite:\n"
                                        "1 - za ponedeljak\n"
                                        "2 - za utorak\n"
                                        "3 - za sredu\n"
                                        "4 - za cetvrtak\n"
                                        "5 - za petak\n"
                                        "6 - za subotu\n"
                                        "7 - za nedelju\n"
                                        "0 - za kraj navodjenja\n"))
                    if first_time and weekday == 0:
                        print("Mora biti bar jedan dan projektovanja!\n")
                        continue
                    elif weekday == 0:
                        first_time = False
                        break
                    elif weekday > 7 or weekday < 0:
                        print("Greska! \n")
                        continue
                    else:
                        no_repetition = True
                        if weekdays:
                            for i in weekdays:
                                if i == weekday:
                                    no_repetition = False
                                    break
                        if not no_repetition:
                            print("Ne smete uneti isti dan dva puta!\n")
                            continue
                        else:
                            first_time = False
                            weekdays.append(weekday)


            except ValueError:
                print("Pogresan unos, sad pocnite ispocetka!\n")
                continue

            if (not first_time) and weekdays:
                break
        weekdays.sort()
        weekdays_str = ""
        weekdays_number = len(weekdays)
        current = 0
        for i in weekdays:
            if i == 1:
                weekdays_str += "ponedeljak"
            elif i == 2:
                weekdays_str += "utorak"
            elif i == 3:
                weekdays_str += "sreda"
            elif i == 4:
                weekdays_str += "cetvrtak"
            elif i == 5:
                weekdays_str += "petak"
            elif i == 6:
                weekdays_str += "subota"
            elif i == 7:
                weekdays_str += "nedelja"
            current += 1
            if current < weekdays_number:
                weekdays_str += ","

        display_all_films()
        while True:
            film_name = input("Unesite ime filma: ")
            if unique_test(film_name,films) == 0:
                break
            else:
                print("Nepostojeci film, pogledajte tabelu iznad\n")

        while True:
            try:
                price = int(input("Unesite osnovnu cenu karte projekcije u dinarima: "))
                if price < 100 or price > 10000:
                    print("Cena mora biti izmedju 100 i 10000 dinara!\n")
                    continue
                break
            except ValueError:
                print("Los unos\n")
                continue
        price_str = str(price)
        new_projection = [str(id_projection), hall, time_start, time_end, weekdays_str, film_name, price_str]
        projections.append(new_projection)

        delete_next_2w_pt()
        generate_pt()

    elif option == 2:
        display_projections()
        while True:
                proj_id = input("Unesite sifru projekcije: ")
                if unique_test(proj_id, projections) == 0:
                    break
                elif proj_id == "x":
                    return
                else:
                    print("Nepostojeca projekcija, pogledajte iznad! (za odustajanje ukucajte x)\n")
                    continue
        while True:
            hall = input("Unesite sifru sale: ")
            if unique_test(hall, halls) == 0:
                break
            else:
                print("Nepostojeca sala\n")
        while True:
            time_start = input("Unesite vreme pocetka u formatu HH:MM: ")
            try:
                hours = int(time_start.split(":")[0])
                minutes = int(time_start.split(":")[1])
                if hours < 0 or hours > 24 or minutes > 59 or minutes < 0:
                    print("Pogresan unos\n")
                    continue
                else:
                    break
            except:
                print("Pogresan unos\n")
                continue
        while True:
            time_end = input("Unesite vreme kraja u formatu HH:MM: ")
            try:
                hours = int(time_end.split(":")[0])
                minutes = int(time_end.split(":")[1])
                if hours < 0 or hours > 24 or minutes > 59 or minutes < 0:
                    print("Pogresan unos\n")
                    continue
                else:
                    break
            except:
                print("Pogresan unos\n")
                continue
        while True:
            weekdays = []
            try:
                first_time = True
                while True:
                    weekday = int(input("Unesite:\n"
                                        "1 - za ponedeljak\n"
                                        "2 - za utorak\n"
                                        "3 - za sredu\n"
                                        "4 - za cetvrtak\n"
                                        "5 - za petak\n"
                                        "6 - za subotu\n"
                                        "7 - za nedelju\n"
                                        "0 - za kraj navodjenja\n"))
                    if first_time and weekday == 0:
                        print("Mora biti bar jedan dan projektovanja!\n")
                        continue
                    elif weekday == 0:
                        first_time = False
                        break
                    elif weekday > 7 or weekday < 0:
                        print("Greska! \n")
                        continue
                    else:
                        no_repetition = True
                        if weekdays:
                            for i in weekdays:
                                if i == weekday:
                                    no_repetition = False
                                    break
                        if not no_repetition:
                            print("Ne smete uneti isti dan dva puta!\n")
                            continue
                        else:
                            first_time = False
                            weekdays.append(weekday)


            except ValueError:
                print("Pogresan unos, sad pocnite ispocetka!\n")
                continue

            if (not first_time) and weekdays:
                break
        weekdays.sort()
        weekdays_str = ""
        weekdays_number = len(weekdays)
        current = 0
        for i in weekdays:
            if i == 1:
                weekdays_str += "ponedeljak"
            elif i == 2:
                weekdays_str += "utorak"
            elif i == 3:
                weekdays_str += "sreda"
            elif i == 4:
                weekdays_str += "cetvrtak"
            elif i == 5:
                weekdays_str += "petak"
            elif i == 6:
                weekdays_str += "subota"
            elif i == 7:
                weekdays_str += "nedelja"
            current += 1
            if current < weekdays_number:
                weekdays_str += ","

        display_all_films()
        while True:
            film_name = input("Unesite ime filma: ")
            if unique_test(film_name,films) == 0:
                break
            else:
                print("Nepostojeci film, pogledajte tabelu iznad\n")

        while True:
            try:
                price = int(input("Unesite osnovnu cenu karte projekcije u dinarima: "))
                if price < 100 or price > 10000:
                    print("Cena mora biti izmedju 100 i 10000 dinara!\n")
                    continue
                break
            except ValueError:
                print("Los unos\n")
                continue
        price_str = str(price)
        new_projection = [proj_id, hall, time_start, time_end, weekdays_str, film_name, price_str]

        edited_index = index_finder(proj_id, projections)
        projections[edited_index] = new_projection

        delete_next_2w_pt()
        generate_pt()

    elif option == 3:
        display_projections()
        while True:
            proj_id = input("Unesite sifru projekcije koju brisete (x za odustajanje): ")
            if unique_test(proj_id, projections) == 0:
                break
            elif proj_id == "x":
                return
            else:
                print("Nepostojeca projekcija, za odustajanje ukucajte x\n")
                continue
        deleting_index = index_finder(proj_id, projections)
        projections[deleting_index] = [projections[deleting_index][0],"x","x","x","x","x","x"]

        delete_next_2w_pt()
        generate_pt()

        delete_reserved_for(projections[deleting_index][0])


def less_than_month(date_str):
    date = datetime.strptime(date_str, "%d.%m.%Y.").date()
    today = datetime.today().date()
    diff = today - date
    numday = diff.days
    if numday < 30:
        return True
    return  False


def report_making():
    while True:
        try:
            option = int(input("1 - Lista prodatih karata za odabran datum prodaje\n"
                               "2 - Lista prodatih karata za odabran datum termina bioskopske projekcije\n"
                               "3 - Lista prodatih karata za odabran datum prodaje i odabranog prodavca\n"
                               "4 - Ukupan broj i ukupna cena prodatih karata za izabran dan (u nedelji) prodaje\n"
                               "5 - Ukupan broj i ukupna cena prodatih karata za izabran dan (u nedelji) održavanja projekcije\n"
                               "6 - Ukupna cena prodatih karata za zadati film u svim projekcijama\n"
                               "7 - Ukupan broj i ukupna cena prodatih karata za izabran dan prodaje i odabranog prodavca\n"
                               "8 - Ukupan broj i ukupna cena prodatih karata po prodavcima (za svakog prodavca) u poslednjih 30 dana\n"
                               "0 - nazad\n"))
            if option > 8 or option < 0:
                print("Nevalidan unos!\n")
                continue
        except ValueError:
            print("Nevalidan unos!\n")
            continue
        if option == 0:
            return
        elif option == 1:
            rep = []
            qdate = input("Unesite zeljeni datum u formatu DD.MM.YYYY. : ")
            one_found = False
            for ticket in tickets:
                if qdate == ticket[5] and ticket[6] == "1":
                    if not one_found:
                        print("*" * 150)
                        print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(
                            "Projekcija: ", "Film: ", "Datum: ", "Pocetak: ",
                            "Kraj: ", "Sediste: ", "Prodata: ", "Sifra karte: "))
                    one_found = True
                    display_one_ticket(ticket)
                    rep.append(ticket)
            if not one_found:
                print("Nema karata za odabrani datum\n")
            else:
                print("*"*150)

                save_rep = input("Unesite 's' ako zelite da sacuvate ovaj izvestaj, enter ako ne zelite.")
                if save_rep == "s":
                    pack_in(rep, "reports/rep_1.txt")

        elif option == 2:
            rep = []
            qdate = input("Unesite zeljeni datum u formatu DD.MM.YYYY. : ")
            one_found = False
            for ticket in tickets:
                for proj_time in projection_times:
                    if proj_time[0] == ticket[3] and qdate == proj_time[1]:
                        if not one_found:
                            print("*" * 150)
                            print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(
                                  "Projekcija: ", "Film: ", "Datum: ", "Pocetak: ",
                                  "Kraj: ", "Sediste: ", "Prodata: ", "Sifra karte: "))
                        one_found = True
                        display_one_ticket(ticket)
                        rep.append(ticket)
            if not one_found:
                print("Nema karata za odabrani datum\n")
            else:
                print("*"*150)
                save_rep = input("Unesite 's' ako zelite da sacuvate ovaj izvestaj, enter ako ne zelite.")
                if save_rep == "s":
                    pack_in(rep, "reports/rep_2.txt")

        elif option == 3:
            rep = []
            qdate = input("Unesite zeljeni datum u formatu DD.MM.YYYY. : ")
            while True:
                q_salesman = input("Unesite korisnicko ime prodavca: ")
                if unique_test(q_salesman, users) == 0:
                    user_index = index_finder(q_salesman, users)
                    if users[user_index][4] != "prodavac":
                        print("Korisnik nije prodavac!\n")
                    else:
                        break
            one_found = False
            for ticket in tickets:
                for sale in sales:
                    if qdate == sale[3] and q_salesman == sale[2] and sale[0]==ticket[0]:
                        if not one_found:
                            print("*" * 150)
                            print("{0:14}|{1:30}|{2:15}|{3:10}|{4:8}|{5:10}|{6:10}|{7:8}\n".format(
                                    "Projekcija: ", "Film: ", "Datum: ", "Pocetak: ",
                                    "Kraj: ", "Sediste: ", "Prodata: ", "Sifra karte: "))
                        one_found = True
                        display_one_ticket(ticket)
                        rep.append(ticket)
            if not one_found:
                print("Nema karata za odabrani datum\n")
            else:
                print("*"*150)
                save_rep = input("Unesite 's' ako zelite da sacuvate ovaj izvestaj, enter ako ne zelite.")
                if save_rep == "s":
                    pack_in(rep, "reports/rep_3.txt")
        elif option == 4:
            try:
                weekday = int(input("Unesite:\n"
                                    "1 - za ponedeljak\n"
                                    "2 - za utorak\n"
                                    "3 - za sredu\n"
                                    "4 - za cetvrtak\n"
                                    "5 - za petak\n"
                                    "6 - za subotu\n"
                                    "7 - za nedelju\n"))
                if weekday>7 or weekday<1:
                    print("Pogresan unos.\n")
                    continue
            except ValueError:
                print("Pogresan unos.\n")
                continue
            weekday_str = ""
            if weekday == 1:
                weekday_str = "Mon"
            elif weekday == 2:
                weekday_str = "Tue"
            elif weekday == 3:
                weekday_str = "Wed"
            elif weekday == 4:
                weekday_str = "Thu"
            elif weekday == 5:
                weekday_str = "Fri"
            elif weekday == 6:
                weekday_str = "Sat"
            elif weekday == 7:
                weekday_str = "Sun"

            ticket_num = 0
            sum = 0.0

            for sale in sales:
                sale_date = datetime.strptime(sale[3], "%d.%m.%Y.")
                sale_weekday = sale_date.strftime("%a")
                if weekday_str == sale_weekday:
                    ticket_num += 1
                    sum += float(sale[1])
            print(str(weekday) + "-tog dana u nedelji je prodato " + str(ticket_num) + " karata po ukupnoj ceni od " + str(sum) + " dinara\n")
            save_rep = input("Unesite 's' ako zelite da sacuvate ovaj izvestaj, enter ako ne zelite.")
            if save_rep == "s":
                with open('reports/rep_4.txt', 'w') as rep_file:
                    rep_file.write(str(weekday) + "-tog dana u nedelji je prodato " + str(ticket_num) + " karata po ukupnoj ceni od " + str(sum) + " dinara\n")
        elif option == 5:
            try:
                weekday = int(input("Unesite:\n"
                                    "1 - za ponedeljak\n"
                                    "2 - za utorak\n"
                                    "3 - za sredu\n"
                                    "4 - za cetvrtak\n"
                                    "5 - za petak\n"
                                    "6 - za subotu\n"
                                    "7 - za nedelju\n"))
                if weekday>7 or weekday<1:
                    print("Pogresan unos.\n")
                    continue
            except ValueError:
                print("Pogresan unos.\n")
                continue
            weekday_str = ""
            if weekday == 1:
                weekday_str = "Mon"
            elif weekday == 2:
                weekday_str = "Tue"
            elif weekday == 3:
                weekday_str = "Wed"
            elif weekday == 4:
                weekday_str = "Thu"
            elif weekday == 5:
                weekday_str = "Fri"
            elif weekday == 6:
                weekday_str = "Sat"
            elif weekday == 7:
                weekday_str = "Sun"

            ticket_num = 0
            sum = 0.0
            for sale in sales:
                for pr_time in projection_times:
                    for ticket in tickets:
                        if sale[0] == ticket[0] and ticket[3] == pr_time[0]:
                            pr_date = datetime.strptime(pr_time[1], "%d.%m.%Y.")
                            pr_weekday = pr_date.strftime("%a")
                            if pr_weekday == weekday_str:
                                ticket_num += 1
                                sum += float(sale[1])
            print(str(weekday) + "-tog dana u nedelji je prodato " + str(ticket_num) + " karata po ukupnoj ceni od " + str(sum) + " dinara\n")
            save_rep = input("Unesite 's' ako zelite da sacuvate ovaj izvestaj, enter ako ne zelite.")
            if save_rep == "s":
                with open('reports/rep_5.txt', 'w') as rep_file:
                    rep_file.write(str(weekday) + "-tog dana u nedelji je prodato " + str(ticket_num) + " karata po ukupnoj ceni od " + str(sum) + " dinara\n")
        elif option == 6:
            display_all_films()
            while True:
                filmname = input("Unesite ime filma: ")
                if unique_test(filmname, films) == 0:
                    break
                else:
                    print("Nepostojeci film.\n")

            sum = 0.0
            for projection in projections:
                for ticket in tickets:
                    if projection[0] == ticket[3][:4] and filmname == projection[5]:
                        for sale in sales:
                            if sale[0] == ticket[0]:
                                sum += float(sale[1])
            print("Za film " + filmname + " je kupljena vrednost karata " + str(sum) + "\n")
            save_rep = input("Unesite 's' ako zelite da sacuvate ovaj izvestaj, enter ako ne zelite.")
            if save_rep == "s":
                with open('reports/rep_6.txt', 'w') as rep_file:
                    rep_file.write("Za film " + filmname + " je kupljena vrednost karata "+ str(sum) + "\n")
        elif option == 7:
            while True:
                qdate = input("Unesite datum u formatu DD.MM.YYYY.: ")
                if len(qdate) != 11:
                    print("los format\n")
                    continue
                break
            while True:
                q_salesman = input("Unesite korisnicko ime prodavca: ")
                if unique_test(q_salesman, users) == 0:
                    user_index = index_finder(q_salesman, users)
                    if users[user_index][4] != "prodavac":
                        print("Korisnik nije prodavac!\n")
                    else:
                        break

            sum = 0.0
            ticket_num = 0
            for ticket in tickets:
                if ticket[5] == qdate:
                    for sale in sales:
                        if sale[0] == ticket[0] and sale[2] == q_salesman:
                            ticket_num += 1
                            sum += float(sale[1])
            print("Za datum " + qdate + " i prodavca " + q_salesman + " prodato je " + str(ticket_num) + " karata po ceni od " + str(sum) + " dinara\n")
            save_rep = input("Unesite 's' ako zelite da sacuvate ovaj izvestaj, enter ako ne zelite.")
            if save_rep == "s":
                with open('reports/rep_7.txt', 'w') as rep_file:
                    rep_file.write("Za datum " + qdate + " i prodavca " + q_salesman + " prodato je " + str(ticket_num) + " karata po ceni od " + str(sum) + " dinara\n")
        elif option == 8:
            salesmen = []
            for user in users:
                if user[4] == "prodavac":
                    salesmen.append([user[0], 0, 0.0])
            rep = []
            for sale in sales:
                for salesman in salesmen:
                    if sale[2] == salesman[0] and less_than_month(sale[3]):
                        salesman[1] += 1
                        salesman[2] += float(sale[1])
            print("{0:20}|{1:15}|{2:15}\n".format("Prodavac: ", "Broj karata: ", "Cena: "))
            for salesman in salesmen:
                print("{0:20}|{1:15}|{2:15}\n".format(salesman[0], salesman[1], salesman[2]))
                rep.append([salesman[0], str(salesman[1]), str(salesman[2])])
            save_rep = input("Unesite 's' ako zelite da sacuvate ovaj izvestaj, enter ako ne zelite.")
            if save_rep == "s":
                pack_in(rep, "reports/rep_8.txt")

        else:
            return


def kupac_menu(user, list):
    correct = 0
    logged = 1
    option = -1
    while logged == 1:
        while correct == 0:
            try:
                option = int(input("Kupac meni:\n"
                                   "1 - za rezervaciju karata           \n"
                                   "2 - za promenu licnih podataka      \n"
                                   "3 - za pregled dostupnih filmova    \n"
                                   "4 - za pretragu filmova ukucajte    \n"
                                   "5 - za pretragu termina projekcija  \n"
                                   "6 - za pregled Vasih karata         \n"
                                   "7 - za ponistavanje Vasih karata    \n"
                                   "0 - za logout                       \n"))
            except ValueError:
                print("POGRESAN UNOS, POKUSAJTE PONOVO: \n")
                correct = 0
                continue
            if 0 <= option <= 6:
                correct = 1
            else:
                print("POGRESAN UNOS, MORA BITI IZMEDJU 0 I 5, POKUSAJTE PONOVO: \n")

            # ovde je korisnik uspesno odabrao neku od opcija

            if option == 0:
                logged = 0
            elif option == 1:
                ticket_reservation(user)
                correct = 0
            elif option == 2:
                userinfo_change(user, list)
                correct = 0
            elif option == 3:
                display_all_films()
                correct = 0
            elif option == 4:
                film_search()
                correct = 0
            elif option == 5:
                projection_time_search()
                correct = 0
            elif option == 6:
                display_my_tickets(user)
                correct = 0
            elif option == 7:
                display_my_tickets(user)
                ticket_id = input("Izaberite kartu koju cete ponistiti: ")
                if valid_ticket_for_user_delete(user[0], ticket_id):
                    ticket_delete(ticket_id)
                    print("Karta {0} je uspesno obrisana".format(ticket_id))
            else:
                print("uskoro...\n")
                correct = 0


def prodavac_menu(user, list):
    correct = 0
    logged = 1
    while logged == 1:
        while correct == 0:
            try:
                option = int(input("Prodavac meni:\n"
                                   "1 za pregled rezervacija \n"
                                   "2 za promenu licnih podataka\n"
                                   "3 za pregled dostupnih filmova \n"
                                   "4 za pretragu filmova \n"
                                   "5 za pretragu termina projekcija\n"
                                   "6 za rezervaciju karata\n"
                                   "7 za prodaju rezervisane karte\n"
                                   "8 za izmene rezervacija\n"
                                   "9 za ponistavanje rezervacija/prodatih karata\n"
                                   "10 za pretragu karata\n"
                                   "11 za direktnu prodaju karata\n"
                                   "12 za automatsko ponistavanje rezervacija\n"
                                   "0 za logout  \n"))
            except ValueError:
                print("POGRESAN UNOS, POKUSAJTE PONOVO: \n")
                correct = 0
                continue
            if 0 <= option <= 12:
                correct = 1
            else:
                print("POGRESAN UNOS MORA BITI IZMEDJU 0 I 12, POKUSAJTE PONOVO: \n")

            # ovde je korisnik uspesno odabrao neku od opcija

            if option == 0:
                logged = 0
            elif option == 1:
                display_all_tickets()
                correct = 0
            elif option == 2:
                userinfo_change(user, list)
                correct = 0
            elif option == 3:
                display_all_films()
                correct = 0
            elif option == 4:
                film_search()
                correct = 0
            elif option == 5:
                projection_time_search()
                correct = 0
            elif option == 6:
                ticket_reservation(user)
                correct = 0
            elif option == 7:
                ticket_selling(user[0])
                correct = 0
            elif option == 8:
                ticket_change()
                correct = 0
            elif option == 9:
                ticket_delete()
                correct = 0
            elif option == 10:
                ticket_search()
                correct = 0
            elif option == 11:
                direct_ticket_sell(user[0])
                correct = 0
            elif option == 12:
                automatic_delete_reservations()
                correct = 0
            else:
                print("uskoro...\n")
                correct = 0


def menadzer_menu(user, list):
    correct = 0
    logged = 1
    while logged == 1:
        while correct == 0:
            try:
                option = int(input("Menadzer meni:\n"
                                   "1 - za registraciju novih prodavaca\n"
                                   "2 - za registraciju novih menadzera\n"
                                   "3 - za prikaz izvestaja\n"
                                   "4 - za izmenu licnih podataka \n"
                                   "5 - za pregled dostupnih filmova \n"
                                   "6 - za pretragu filmova \n"
                                   "7 - za pretragu termina projekcija\n"
                                   "8 - za prikaz slobodnih sedista za odredjenu projekciju\n"
                                   "9 - za dodavanje/izmenu/brisanje filmova\n"
                                   "10 - za dodavanje/izmenu/brisanje projekcija\n"
                                   "11 - za izradu kartice lojalnosti\n"
                                   "0 - za logout  \n"))
            except ValueError:
                print("POGRESAN UNOS, POKUSAJTE PONOVO: \n")
                correct = 0
                continue
            if 0 <= option <= 11:
                correct = 1
            else:
                print("POGRESAN UNOS MORA BITI IZMEDJU 0 I 10, POKUSAJTE PONOVO: \n")
                correct = 0
                continue
            # uspesno odabrana opcija

            if option == 0:
                logged = 0
            elif option == 1:
                user_id = input("Unesite korisnicko ime: ")
                while unique_test(user_id, users) == 0 or user_id == "":
                    user_id = input("Vec postojano, probajte ponovo: ")
                password = input("Unesite svoj password: ")
                while password_test(password) == 0:
                    password = input("Password mora biti duzi od 6 karaktera i sa bar jednom cifrom, "
                                     "pokusajte ponovo: ")
                ime = input("Unesite svoje ime: ")
                prezime = input("Unesite svoje prezime: ")
                register(user_id, password, ime, prezime, "prodavac", users)
                correct = 0
            elif option == 2:
                user_id = input("Unesite korisnicko ime: ")
                while unique_test(user_id, users) == 0 or user_id == "":
                    user_id = input("Vec postojano, probajte ponovo: ")
                password = input("Unesite svoj password: ")
                while password_test(password) == 0:
                    password = input("Password mora biti duzi od 6 karaktera i sa bar jednom cifrom, "
                                     "pokusajte ponovo: ")
                ime = input("Unesite svoje ime: ")
                while ime == "":
                    ime = input("Ime ne moze biti prazno, unesite svoje ime: ")
                prezime = input("Unesite svoje prezime: ")
                while prezime == "":
                    prezime = input("Prezime ne moze biti prazno, unesite svoje prezime: ")
                register(user_id, password, ime, prezime, "menadzer", users)
                correct = 0
            elif option == 3:
                report_making()
                correct = 0
            elif option == 4:
                userinfo_change(user, list)
                correct = 0
            elif option == 5:
                display_all_films()
                correct = 0
            elif option == 6:
                film_search()
                correct = 0
            elif option == 7:
                projection_time_search()
                correct = 0
            elif option == 8:
                display_matrix_seats()
                correct = 0
            elif option == 9:
                repertoire_change()
                correct = 0
            elif option == 10:
                projection_change()
                correct = 0
            elif option == 11:
                create_loyalty_card()
                correct = 0
            else:
                print("uskoro...")
                correct = 0


def userinfo_change(user, list):
    index = index_finder(user[0], list)
    user[1] = input("Novi password: ")
    while password_test(user[1]) == 0:
        user[1] = input("Password mora biti duzi od 6 karaktera i sa bar jednom cifrom, pokusajte ponovo: ")
    user[2] = input("Novo ime: ")
    while user[2] == "":
        user[2] = input("Ime ne moze biti prazno: ")

    user[3] = input("Novo prezime: ")
    while user[3] == "":
        user[3] = input("Ime ne moze biti prazno: ")

    list[index] = user


if __name__ == '__main__':

    
    users = unpack("users.txt")
    films = unpack("films.txt")
    projections = unpack("projections.txt")
    halls = unpack("halls.txt")
    projections = unpack("projections.txt")
    projection_times = unpack("projection_times.txt")
    tickets = unpack("tickets.txt")
    loyalty_cards = unpack("loyalty_cards.txt")
    sales = unpack("sales.txt")

    generate_pt()

    exit_operand = 1
    option = -1
    while exit_operand > 0:
        korektan = 0
        while korektan == 0:
            try:
                option = int(input("Meni:\n"
                                   "Za logovanje ukucajte                   1\n"
                                   "Za registraciju kao kupac ukucajte      2\n"
                                   "Za pregled dostupnih filmova ukucajte   3\n"
                                   "Za pretragu filmova ukucajte            4\n"
                                   "Za pretragu termina projekcija ukucajte 5\n"
                                   "Za izlaz ukucajte                       0\n"))
            except ValueError:
                print("POGRESAN UNOS, POKUSAJTE PONOVO: \n")
                korektan = 0
                continue
            if 0 <= option <= 5:
                korektan = 1
            else:
                print("POGRESAN UNOS MORA BITI IZMEDJU 0 I 5, POKUSAJTE PONOVO: \n")

        # sad je uneta opcija pocetnog menija

        if option == 2:

            user_id = input("Unesite korisnicko ime: ")
            while unique_test(user_id, users) == 0 or user_id == "":
                user_id = input("Vec postojano, probajte ponovo: ")
            password = input("Unesite svoj password: ")
            while password_test(password) == 0:
                password = input("Password mora biti duzi od 6 karaktera i sa bar jednom cifrom, "
                                 "pokusajte ponovo: ")
            ime = input("Unesite svoje ime: ")
            while ime == "":
                ime = input("Ime ne moze biti prazno, unesite svoje ime: ")
            prezime = input("Unesite svoje prezime: ")
            while prezime == "":
                prezime = input("Prezime ne moze biti prazno, unesite svoje prezime: ")
            register(user_id, password, ime, prezime, "kupac", users)

        elif option == 1:
            user_id = input("Unesite korisnicko ime: ")
            while unique_test(user_id, users) == 1:
                user_id = input("Korisnicko ime ne postoji u sistemu, probajte ponovo: ")
            password = input("Unesite svoj password: ")
            while password_matching(user_id, password, users) == 0:
                password = input("Probajte ponovo: ")
            login(user_id, users)
        elif option == 3:
            display_all_films()
            korektan = 0
        elif option == 4:
            film_search()
            korektan = 0
        elif option == 5:
            projection_time_search()
            korektan = 0
        elif option == 0:
            exit_operand = 0
            pack_in(users, "user.txt")
            pack_in(films, "films.txt")
            pack_in(projections, "projections.txt")
            pack_in(projection_times, "projection_times.txt")
            pack_in(tickets, "tickets.txt")
            pack_in(loyalty_cards, "loyalty_cards.txt")
            pack_in(sales, "sales.txt")

            print("izasao")
