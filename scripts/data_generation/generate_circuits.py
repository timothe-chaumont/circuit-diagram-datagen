import numpy as np

# later : use objects instead of dictionnaries

BIPOLE_TOKENS = ["short", "open", "generic",
                 "capacitor", "cute inductor",
                 "battery1", "european voltage source", "european current source",
                 "ammeter", "voltmeter",
                 "normal open switch"]


def generate_one_loop_circuit(bipole_tokens=BIPOLE_TOKENS):
    """Generates an eletrical circuit in the form of a list of bipole elements
       The generated circuits are composed of one single loop

       generate a random size for corresponding segments, and then generate a random number of elements

       Returns:
          A list of dictionnaries with keys : 
          - "from" : the position of the before node
          - "to" : the position of the after node
          - "type" : the kind of electrical bipole 
    """
    segments_list = []
    nb_vert_segments = 2
    nb_horiz_segments = 2
    # generate the 'shape' of the circuit
    vert_max_nb_elts, horiz_max_nb_elts = np.random.randint(1, 4, size=2)

    # bottom & top segments
    for s in range(nb_horiz_segments):
        y_pos = 2*s
        nb_elements = np.random.randint(1, horiz_max_nb_elts+1)
        for e in range(nb_elements):
            bipole = np.random.choice(bipole_tokens)
            element = {"from": (2*e, y_pos), "to": (2*e +
                                                    2, y_pos), "type": bipole}
            segments_list.append(element)

    # left & right segment
    for s in range(nb_vert_segments):
        x_pos = 2*s
        nb_elements = np.random.randint(1, vert_max_nb_elts+1)
        for e in range(nb_elements):
            bipole = np.random.choice(bipole_tokens)
            element = {"from": (x_pos, 2*e), "to": (x_pos,
                                                    2*e + 2), "type": bipole}
            segments_list.append(element)

    return segments_list


# tests
if __name__ == "__main__":
    print(generate_one_loop_circuit())
