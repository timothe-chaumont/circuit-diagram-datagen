import numpy as np


BIPOLE_TOKENS = ["short", "open", "generic",
                 "capacitor", "cute inductor",
                 "battery1", "european voltage source", "european current source",
                 "ammeter", "voltmeter",
                 "normal open switch"]


def generate_one_loop_circuit():
    """Generates an eletrical circuit in the form of a tokens list 
       These circuits are composed of a single loop

       generate a random size for corresponding segments, and then generate a random number of elements
    """
    segments_list = []
    nb_segments = 4
    # generate the 'shape' of the circuit
    vert_max_nb_elts, horiz_max_nb_elts = np.random.randint(1, 4, size=2)

    # bottom segment
    nb_elements = np.random.randint(1, horiz_max_nb_elts+1)
    for e in range(nb_elements):
        bipole = np.random.choice(BIPOLE_TOKENS)
        element = {"from": (2*e, 0), "to": (2*e + 2, 0), "type": bipole}
        segments_list.append(element)

    # left segment
    nb_elements = np.random.randint(1, vert_max_nb_elts+1)
    for e in range(nb_elements):
        bipole = np.random.choice(BIPOLE_TOKENS)
        element = {"from": (0, 2*e), "to": (0, 2*e + 2), "type": bipole}
        segments_list.append(element)

    # top segment
    nb_elements = np.random.randint(1, horiz_max_nb_elts+1)
    y_pos = vert_max_nb_elts * 2
    for e in range(nb_elements):
        bipole = np.random.choice(BIPOLE_TOKENS)
        element = {"from": (2*e, y_pos), "to": (2*e + 2,
                                                y_pos), "type": bipole}
        segments_list.append(element)

    # right segment
    nb_elements = np.random.randint(1, vert_max_nb_elts+1)
    x_pos = horiz_max_nb_elts * 2
    for e in range(nb_elements):
        bipole = np.random.choice(BIPOLE_TOKENS)
        element = {"from": (x_pos, 2*e), "to": (x_pos,
                                                2*e + 2), "type": bipole}
        segments_list.append(element)

    return segments_list


# tests
if __name__ == "__main__":
    print(generate_one_loop_circuit())
