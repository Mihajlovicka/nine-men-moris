from hashmap import ChainedHashMap
import copy
from tree import GameNode,Tree
from time import time
pozicije = ChainedHashMap(24)
pozicije['00'] = 0
pozicije['03'] = 1
pozicije['06'] = 2
pozicije['11'] = 3
pozicije['13'] = 4
pozicije['15'] = 5
pozicije['22'] = 6
pozicije['23'] = 7
pozicije['24'] = 8
pozicije['30'] = 9
pozicije['31'] = 10
pozicije['32'] = 11
pozicije['34'] = 12
pozicije['35'] = 13
pozicije['36'] = 14
pozicije['42'] = 15
pozicije['43'] = 16
pozicije['44'] = 17
pozicije['51'] = 18
pozicije['53'] = 19
pozicije['55'] = 20
pozicije['60'] = 21
pozicije['63'] = 22
pozicije['66'] = 23
moris_formacije = [[[1,2],[9,21]],[[0,2],[4,7]],[[0,1],[14,23]],[[4,5],[10,18]],[[3,5],[1,7]],[[3,4],[13,20]],[[7,8],[11,15]],[[1,4],[6,8]],[[6,7],[12,17]],
                   [[0,21],[10,11]],[[3,18],[9,11]],[[6,15],[9,10]],[[8,17],[13,14]],[[5,20],[12,14]],[[2,23],[12,13]],[[6,11],[16,17]],[[15,17],[19,22]],
                   [[15,16],[8,12]],[[3,10],[19,20]],[[16,22],[18,20]],[[5,13],[18,19]],[[0,9],[22,23]],[[16,19],[21,23]],[[2,14],[21,22]]]
susedni = [[1,9],[0,2,4],[1,14],[4,10],[1,3,5,7],[4,13],[7,11],[4,6,8],[7,12],[0,10,21],[3,9,11,18],[6,10,15],[8,13,17],[5,12,14,20],[2,13,23],
           [11,16],[15,17,19],[12,16],[10,19],[16,18,20,22],[13,19],[9,22],[19,21,23],[14,22]]
WHITE = 'W'
BLACK = 'B'

def napravi_tablu():
    return ['O'] * 24

def hackerranktabla(string):
    tabla = [None] * 24
    j = 0
    for i in string:
        for ch in i:
            if ch == "O" or ch == "W" or ch == "B":
                tabla[j] = ch
                j += 1
    return tabla


def nacrtaj_tablu(tabla):
    print('6 {}--------------{}--------------{}'.format(tabla[21], tabla[22], tabla[23]))
    print('  |              |              |')
    print('5 |    {}---------{}---------{}    |'.format(tabla[18], tabla[19], tabla[20]))
    print('  |    |         |         |    |')
    print('4 |    |    {}----{}----{}    |    |'.format(tabla[15], tabla[16], tabla[17]))
    print('  |    |    |         |    |    |')
    print('3 {}----{}----{}         {}----{}----{}'.format(tabla[9], tabla[10], tabla[11],
                                                           tabla[12], tabla[13], tabla[14]))
    print('  |    |    |         |    |    |')
    print('2 |    |    {}----{}----{}    |    |'.format(tabla[6], tabla[7], tabla[8]))
    print('  |    |         |         |    |')
    print('1 |    {}---------{}---------{}    |'.format(tabla[3], tabla[4], tabla[5]))
    print('  |              |              |')
    print('0 {}--------------{}--------------{}'.format(tabla[0], tabla[1], tabla[2]))
    print('  0    1    2    3    4    5    6')

def unos_novog_polja(tabla):
    while True:
        polje = input('Unesi polje >> ')
        if polje in pozicije and tabla[pozicije[polje]] == 'O':
            return polje
def pomeri_figuru(tabla,igrac):
    while True:
        polje = input('Unesi pocetno polje >> ')
        if polje in pozicije and tabla[pozicije[polje]] == igrac and not da_li_je_zarobljen(tabla,pozicije[polje]):
            while True:
                krajnje_polje = input('Unesi krajnje polje >> ')
                if krajnje_polje in pozicije and tabla[pozicije[krajnje_polje]] == 'O' and pozicije[krajnje_polje] in susedni[pozicije[polje]]:
                    tabla[pozicije[krajnje_polje]] = igrac
                    tabla[pozicije[polje]] = 'O'
                    if da_li_je_moris(tabla,igrac,pozicije[krajnje_polje]):
                        tabla = izbaci_protivnicku_figuru(tabla,igrac)
                    return tabla


def izbaci_protivnicku_figuru(tabla,igrac):
    while True:
        polje = input('Unesi protivnicko polje >> ')

        if polje in pozicije and tabla[pozicije[polje]] == promeni_igraca(igrac):
            if not da_li_je_moris(tabla,promeni_igraca(igrac),pozicije[polje]):
                tabla[pozicije[polje]] = 'O'
                return tabla
            if broj_figura(tabla,promeni_igraca(igrac)) == broj_mica(tabla,promeni_igraca(igrac)) *3:
                tabla[pozicije[polje]] = 'O'
                return tabla

def koja_je_faza(tabla,igrac,prethodna_faza):
    if prethodna_faza == 4:
        return 1
    if broj_figura(tabla,igrac) == 3 and prethodna_faza > 1:
        return 3
    if broj_figura(tabla,igrac) == 9: return 2
    return prethodna_faza




def promeni_igraca(igrac):
    if igrac == WHITE:
        return BLACK
    return WHITE

def nadji_dubinu(faza):
    if faza == 1:
        return 3
    if faza == 2:
        return 4
    if faza == 3:
        return 3

def igraj_faza_1():
    tabla = napravi_tablu()
    nacrtaj_tablu(tabla)
    for i in range(9):
        igrac = WHITE
        while True:
            polje = unos_novog_polja(tabla)
            if polje in pozicije and tabla[pozicije[polje]] == 'O':
                tabla[pozicije[polje]] = igrac
                if da_li_je_moris(tabla,igrac,pozicije[polje]):
                    tabla = izbaci_protivnicku_figuru(tabla,igrac)
                break
            else: print('Polje nije slobodno.')
        igrac = promeni_igraca(igrac)
        tree = Tree()
        root = GameNode(tabla)
        root.player = igrac
        tree.root = root
        start_time = time()
        potez = minimax(nadji_dubinu(1),tree.root,True,float('-inf'), float('inf'),1)
        tabla = potez.parent.data
        nacrtaj_tablu(tabla)
        print(time() - start_time)
    return tabla

def igraj_faza_23(tabla):
    igrac = WHITE
    while True:
        if da_li_je_neko_izgubio(tabla):
            exit()
        else:
            if igrac == WHITE:
                if broj_figura(tabla, igrac) == 3:
                    tabla = preskaci(tabla, igrac)
                else:
                    tabla = pomeri_figuru(tabla,igrac)
                igrac = promeni_igraca(igrac)
            else:
                tree = Tree()
                root = GameNode(tabla)
                root.player = igrac
                tree.root = root
                start_time = time()
                if broj_figura(tabla, igrac) == 3:
                    potez = minimax(nadji_dubinu(3), tree.root, True, float('-inf'), float('inf'), 3)
                else:
                    potez = minimax(nadji_dubinu(2), tree.root, True, float('-inf'), float('inf'), 2)
                tabla = potez.parent.data
                nacrtaj_tablu(tabla)
                print(time() - start_time)
                igrac = promeni_igraca(igrac)

#sl potezi
def preskaci(tabla,igrac):
    while True:
        polje = input('Unesi pocetno polje >> ')
        if polje in pozicije and tabla[pozicije[polje]] == igrac:
            while True:
                krajnje_polje = input('Unesi krajnje polje >> ')
                if krajnje_polje in pozicije and tabla[pozicije[krajnje_polje]] == 'O':
                    tabla[pozicije[krajnje_polje]] = igrac
                    tabla[pozicije[polje]] = 'O'
                    if da_li_je_moris(tabla,igrac,pozicije[krajnje_polje]):
                        tabla = izbaci_protivnicku_figuru(tabla,igrac)
                    return tabla

def izbaci_random_figuru(tabla,igrac):
    potezi = []
    for i in range(len(tabla)):
        if tabla[i] == promeni_igraca(igrac):
            if not da_li_je_moris(tabla,promeni_igraca(igrac),i):
                nov_potez = copy.deepcopy(tabla)
                nov_potez[i] = 'O'
                potezi.append(nov_potez)
    if not potezi:
        if broj_figura(tabla,promeni_igraca(igrac)) == broj_mica(tabla,promeni_igraca(igrac)) *3:
            for i in range(len(tabla)):
                if tabla[i] == promeni_igraca(igrac):
                    nov_potez = copy.deepcopy(tabla)
                    nov_potez[i] = 'O'
                    potezi.append(nov_potez)
    return potezi

def sortiraj(potezi,max_igrac,faza):
    eval = []
    for potez in potezi:
        eval.append([potez,evaluate(potez,faza)])
    if max_igrac:
        for i in range(len(eval) -1):
            for j in range(i+1,len(eval)):
                if eval[i][1] < eval[j][1]:
                    eval[i],eval[j] = eval[j],eval[i]
    else:
        for i in range(len(eval) - 1):
            for j in range(i + 1, len(eval)):
                if eval[i][1] > eval[j][1]:
                    eval[i], eval[j] = eval[j], eval[i]
    sortirano =[]
    for e in eval:
        sortirano.append(e[0])
    return sortirano

def nadji_sledece_poteze(tabla,faza,max_igrac):
    if faza == 1:
        potezi = nadji_poteze_za_cvor_1(tabla.data,tabla.player)
    elif faza == 2:
        potezi = nadji_poteze_za_cvor_2(tabla.data,tabla.player)
    elif faza == 3:
        potezi = nadji_poteze_za_cvor_3(tabla.data,tabla.player)
    elif faza == 4:
        potezi = izbaci_random_figuru(tabla.data,tabla.player)
    for i in range(len(potezi)):
        potezi[i] = GameNode(potezi[i])
        potezi[i].parent = tabla
    return sortiraj(potezi,max_igrac,faza)

def nadji_poteze_za_cvor_1(tabla,igrac):
    potezi = []
    for i in range(len(tabla)):
        if tabla[i] == 'O':
            nov_potez = copy.deepcopy(tabla)
            nov_potez[i] = igrac
            if da_li_je_moris(nov_potez,igrac,i):
                novi_potezi = izbaci_random_figuru(nov_potez,igrac)
                for potez in novi_potezi:
                    potezi.append(potez)
            else:
                potezi.append(nov_potez)
    return potezi

def nadji_poteze_za_cvor_2(tabla,igrac):
    potezi = []
    for i in range(len(tabla)):
        if tabla[i] == igrac:
            for s in susedni[i]:
                if tabla[s] == 'O':
                    nov_potez = copy.deepcopy(tabla)
                    nov_potez[i] = 'O'
                    nov_potez[s] = igrac
                    if da_li_je_moris(nov_potez, igrac, s):
                        novi_potezi = izbaci_random_figuru(nov_potez, igrac)
                        for potez in novi_potezi:
                            potezi.append(potez)
                    else:
                        potezi.append(nov_potez)
    return potezi

def nadji_poteze_za_cvor_3(tabla,igrac):
    potezi = []
    if broj_figura(tabla,igrac) == 2:
        return None
    for i in range(len(tabla)):
        if tabla[i] == igrac:
            for j in range(len(tabla)):
                if tabla[j] == 'O':
                    nov_potez = copy.deepcopy(tabla)
                    nov_potez[i] = 'O'
                    nov_potez[j] = igrac
                    if da_li_je_moris(nov_potez, igrac, i):
                        novi_potezi = izbaci_random_figuru(nov_potez, igrac)
                        for potez in novi_potezi:
                            potezi.append(potez)
                    else:
                        potezi.append(nov_potez)
    return potezi


#eval
def da_li_je_neko_izgubio(tabla):
    if broj_figura(tabla, BLACK) == 2 or da_li_su_sve_figure_zarobljene(tabla, BLACK):
        print('game over')
        print('WHITE  won')
        return True
    elif broj_figura(tabla, WHITE) == 2 or da_li_su_sve_figure_zarobljene(tabla, WHITE):
        print('game over')
        print('BLACK won')
        return True
    return False

def da_li_su_sve_figure_zarobljene(tabla,igrac):
    svi_zarobljeni = 0
    br_fig = broj_figura(tabla,igrac)
    if br_fig != 0:
        for i in range(len(tabla)):
            if tabla[i] == igrac and da_li_je_zarobljen(tabla, i):
                svi_zarobljeni += 1
        if  svi_zarobljeni == broj_figura(tabla, igrac):
            return True
        else: return False
    else: return False

def da_li_je_moris(tabla,igrac,polje):
    morisi = moris_formacije[polje]
    if tabla[morisi[0][0]] == igrac and tabla[morisi[0][1]] == igrac:
        return True
    if tabla[morisi[1][0]] == igrac and tabla[morisi[1][1]] == igrac:
        return True
    return False

def da_li_je_moris_napravljenuprethodnompotezu(tabla_pre,tabla_posle,igrac):
    for i in range(len(tabla_pre)):
        if tabla_pre[i] != tabla_posle[i] and tabla_pre[i] == 'O':
            if da_li_je_moris(tabla_posle,WHITE,i):
                if igrac == WHITE: return -1
                # else: return 1
            if da_li_je_moris(tabla_posle, BLACK, i):
                if igrac == BLACK:
                    return 1
                # else:
                #     return 1
    return 0

def razlika_broja_mica(tabla):
    return broj_mica(tabla,BLACK) - broj_mica(tabla,WHITE)

def broj_mica(tabla,igrac):
    br = 0
    for i in range(len(tabla)):
        if tabla[i] == igrac:
            morisi = moris_formacije[i]
            if tabla[morisi[0][0]] == igrac and tabla[morisi[0][1]] == igrac:
                br +=1
            if tabla[morisi[1][0]] == igrac and tabla[morisi[1][1]] == igrac:
                br +=1
    return br // 3

def razlika_broja_blokiranih_figura(tabla):
    brW = brB = 0
    for i in range(len(tabla)):
        if tabla[i] == WHITE and da_li_je_zarobljen(tabla,i):
            brW += 1
        if tabla[i] == BLACK and da_li_je_zarobljen(tabla,i):
            brB += 1
    return brW - brB

def da_li_je_zarobljen(tabla,polje):
    sus = susedni[polje]
    for s in sus:
        if tabla[s] == 'O':
            return False
    return True

def broj_figura(tabla,igrac):
    i = 0
    for j in range(len(tabla)):
        if tabla[j] == igrac: i +=1
    return i

def razlika_broja_figura(tabla):
    return broj_figura(tabla,BLACK) - broj_figura(tabla,WHITE)

def razlika_broja_2conf(tabla):
    brW = brB = 0
    for i in range(len(tabla)):
        if tabla[i] == WHITE:
            morisi = moris_formacije[i]
            if tabla[morisi[0][0]] == WHITE and  tabla[morisi[0][1]] == 'O' or  tabla[morisi[0][0]] == 'O' and  tabla[morisi[0][1]] == WHITE:
                brW += 1
            if  tabla[morisi[1][0]] == WHITE and  tabla[morisi[1][1]] == 'O' or  tabla[morisi[1][0]] == 'O' and  tabla[morisi[1][1]] == WHITE:
                brW +=1
        if tabla[i] == BLACK:
            morisi = moris_formacije[i]
            if  tabla[morisi[0][0]] == BLACK and  tabla[morisi[0][1]] == 'O' or  tabla[morisi[0][0]] == 'O' and  tabla[morisi[0][1]] == BLACK:
                brB += 1
            if  tabla[morisi[1][0]] == BLACK and  tabla[morisi[1][1]] == 'O' or  tabla[morisi[1][0]] == 'O' and  tabla[morisi[1][1]] == BLACK:
                brB += 1
    return brB // 2 - brW // 2

def razlika_broja_3conf(conf_2):
    return conf_2 // 2

def da_li_je_dupla_trojka(tabla,igrac,polje):
    morisi = moris_formacije[polje]
    if tabla[morisi[0][0]] == igrac and tabla[morisi[0][1]] == igrac and tabla[morisi[1][0]] == igrac and tabla[morisi[1][1]] == igrac:
        return True

def razlika_broja_duplih_vezanih_trojki(tabla):
    brW = brB = 0
    for i in range(len(tabla)):
        if tabla[i] == WHITE:
            if da_li_je_dupla_trojka(tabla,WHITE,i):brW +=1
        if tabla[i] == BLACK:
            if da_li_je_dupla_trojka(tabla,BLACK,i): brB +=1
    return brB - brW

def da_li_gubi(tabla,faza):
    if broj_figura(tabla.data,WHITE) <= 3 and faza>1:
        return 1
    if broj_figura(tabla.data,BLACK) <= 3 and faza>1:
        return -1
    if da_li_su_sve_figure_zarobljene(tabla.data,WHITE):
        return 1
    if da_li_su_sve_figure_zarobljene(tabla.data,BLACK):
        return -1
    return 0

def evaluate(tabla,faza):
    prvo = da_li_je_moris_napravljenuprethodnompotezu(tabla.parent.data,tabla.data,tabla.parent.player)
    drugo = razlika_broja_mica(tabla.data)
    trece = razlika_broja_blokiranih_figura(tabla.data)
    cetvrto = razlika_broja_figura(tabla.data)
    peto = razlika_broja_2conf(tabla.data)
    sesto = razlika_broja_3conf(peto)
    sedmo = razlika_broja_duplih_vezanih_trojki(tabla.data)
    osam = da_li_gubi(tabla,faza)
    if faza == 1: return 18 *  prvo+ 26 * drugo + 1 * trece+ 6 * cetvrto + 12 * peto + 7 * sesto
    elif faza == 2 :return 14 * prvo + 43 * drugo + 10 * trece + 8 * cetvrto +7 * peto+ 42 * sedmo+ 1086 * osam
    else: return 6 * prvo + 10 * peto + sesto + 1190 * osam

def kraj_igre(tabla,faza):
    if ((broj_figura(tabla, BLACK) == 2 or broj_figura(tabla, WHITE) == 2) and faza != 1 and faza != 4) or da_li_su_sve_figure_zarobljene(tabla, BLACK) or\
             da_li_su_sve_figure_zarobljene(tabla, WHITE) :
        return True
    return False

def minimax(dubina, cvor, max_igrac, alpha, beta,faza):
    if dubina == 0 or kraj_igre(cvor.data,faza):
        cvor.evaluation = evaluate(cvor,faza)
        return cvor
    moguci_potezi = nadji_sledece_poteze(cvor, faza, max_igrac)
    if max_igrac:
        najbolji_potez = GameNode(None)
        najbolji_potez.evaluation = float("-inf")
        for potez in moguci_potezi:
            cvor.add_child(potez)
            potez.player = promeni_igraca(cvor.player)
            eval_node = minimax(dubina - 1, potez, False, alpha, beta,koja_je_faza(potez.data,potez.player,faza))
            if najbolji_potez.evaluation < eval_node.evaluation:
                najbolji_potez.evaluation = eval_node.evaluation
                najbolji_potez.data = eval_node.data
                najbolji_potez.parent = potez
            alpha = max(alpha, najbolji_potez.evaluation)
            if beta <= alpha:
                break
        return najbolji_potez
    else:
        najbolji_potez = GameNode(None)
        najbolji_potez.evaluation =  float("inf")
        for potez in moguci_potezi:
            potez.player = promeni_igraca(cvor.player)
            cvor.add_child(potez)
            eval_node = minimax(dubina - 1, potez, True, alpha, beta, koja_je_faza(potez.data,potez.player,faza))
            if najbolji_potez.evaluation > eval_node.evaluation:
                najbolji_potez.evaluation = eval_node.evaluation
                najbolji_potez.data = eval_node.data
                najbolji_potez.parent = potez
            beta = min(beta, najbolji_potez.evaluation)
            if beta <= alpha:
                break
        return najbolji_potez

#hackerrank
def koja_je_pozicija(i):
    for poz in pozicije:
        if pozicije[poz] == i:
            return poz[0] + " " + poz[1]

def nadji_koji_je_potez_odigran(stara,nova,faza,igrac):
    if faza == 'INIT':
        for i in range(24):
            if stara[i] != nova[i] and stara[i] == 'O':
                return koja_je_pozicija(i)
    if faza == 'MILL':
        for i in range(24):
            if stara[i] != nova[i] and nova[i] == 'O':
                return koja_je_pozicija(i)
    if faza == 'MOVE':
        for i in range(24):
            if stara[i] != nova[i] and nova[i] == 'O' and stara[i] == igrac:
                sa = i
            if stara[i] != nova[i] and stara[i] == 'O' and nova[i] == igrac:
                na = i
        return koja_je_pozicija(sa) + " " + koja_je_pozicija(na)

def nextMove(player, move, board):
    tabla = hackerranktabla(board)
    tree = Tree()
    root = GameNode(tabla)
    tree.root = root
    if move == 'INIT':
        if player == WHITE:
            root.player = WHITE
            potez = minimax(2, tree.root, False, float('-inf'), float('inf'), 1)
        else:
            root.player = BLACK
            potez = minimax(2, tree.root, True, float('-inf'), float('inf'), 1)
        return nadji_koji_je_potez_odigran(tabla,potez.parent.data,'INIT',root.player)
    if move == 'MOVE':
        if player == WHITE:
            root.player = WHITE
            if broj_figura(tabla,WHITE) == 3:
                potez = minimax(4, tree.root, False, float('-inf'), float('inf'), 3)
            else:
                potez = minimax(4, tree.root, False, float('-inf'), float('inf'), 2)
        else:
            root.player = BLACK
            if broj_figura(tabla, BLACK) == 3:
                potez = minimax(4, tree.root, True, float('-inf'), float('inf'), 3)
            else:
                potez = minimax(4,tree.root, True, float('-inf'), float('inf'), 2)
        return nadji_koji_je_potez_odigran(tabla,potez.parent.data,'MOVE',root.player)
    if move == 'MILL':
        if player == WHITE:
            root.player = WHITE
            potez = minimax(4, tree.root, False, float('-inf'), float('inf'), 4)
        else:
            root.player = BLACK
            potez = minimax(4, tree.root, True, float('-inf'), float('inf'), 4)
        return nadji_koji_je_potez_odigran(tabla,potez.parent.data,'MILL',root.player)

if __name__ == '__main__':

    # player = input().strip()
    # move = input().strip()
    #
    # board = []
    # for i in range(7):
    #     board.append(input().strip())
    #
    # print(nextMove(player, move, board))
    tabla = igraj_faza_1()
    igraj_faza_23(tabla)
