def parse(filename):
    cond = -1
    nb_som = 0
    sommets = []
    nb_aretes = 0
    adjacences = []

    parse_list = ["Nombre de sommets\n","Sommets\n","Nombre d aretes\n","Aretes\n"]

    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:

            if line in parse_list:
                cond = parse_list.index(line)
                continue

            if cond == 0:
                nb_som = int(line)
                adjacences = [set() for _ in range(nb_som)]
            if cond == 1:
                sommets.append(int(line.rstrip()))
            if cond == 2:
                nb_aretes = int(line)
            if cond == 3:
                couple = line.split()
                (adjacences[int(couple[0])]).add(int(couple[1]))
    
    return nb_som, sommets, nb_aretes, adjacences