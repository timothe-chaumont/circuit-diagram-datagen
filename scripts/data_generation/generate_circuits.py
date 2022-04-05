import numpy as np
import matplotlib.pyplot as plt
import matplotlib

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
          - "label" : the legend of the bipole
        #   - "label_pos" : the position of the legend
    """
    segments_list = []
    nb_vert_segments = 2
    nb_horiz_segments = 2
    # generate the 'shape' of the circuit
    vert_max_nb_elts, horiz_max_nb_elts = np.random.randint(1, 4, size=2)
    # we can deduce the width and height of the circuit
    circuit_width = 2 * horiz_max_nb_elts
    circuit_height = 2 * vert_max_nb_elts

    # bottom & top segments
    for s in range(nb_horiz_segments):
        y_pos = 2*s
        nb_elements = np.random.randint(1, horiz_max_nb_elts+1)
        # deduce, from this number, the spacing between each bipole
        segment_lenth = int(circuit_width / nb_elements)
        for e in range(nb_elements):
            bipole = np.random.choice(bipole_tokens)
            element = {"from": (segment_lenth*e, y_pos), "to": (segment_lenth*e +
                                                                segment_lenth, y_pos), "type": bipole}
            # print(element)
            segments_list.append(element)

    # left & right segment
    for s in range(nb_vert_segments):
        x_pos = 2*s
        nb_elements = np.random.randint(1, vert_max_nb_elts+1)
        segment_lenth = int(circuit_height / nb_elements)
        for e in range(nb_elements):
            bipole = np.random.choice(bipole_tokens)
            element = {"from": (x_pos, segment_lenth*e),
                       "to": (x_pos, segment_lenth*e + segment_lenth),
                       "type": bipole}
            # print(element)
            segments_list.append(element)

    # end segments

    return segments_list
    # degub with tests (display position of each element)


def get_horizontal_lines(y_pos, horiz_spaces):
    """
    """
    lines_list = []
    # x starts at 0 and increases to the right
    current_x_pos = 0
    # for each segment (we go through each size)
    for x_space in horiz_spaces:
        start_x = current_x_pos
        end_x = start_x + x_space

        lines_list.append(
            {"from": (start_x, y_pos), "to": (end_x, y_pos)}
        )

        # update the new starting point
        current_x_pos = end_x

    return lines_list


def get_vertical_lines(y_start, y_end, horiz_spaces):
    lines_list = []
    # x starts at 0 and increases to the right
    current_x_pos = 0
    # for each segment (we go through each size)
    for x_space in horiz_spaces:
        lines_list.append(
            {"from": (current_x_pos, y_start), "to": (current_x_pos, y_end)}
        )

        # update the new starting point
        current_x_pos += x_space
    lines_list.append(
        {"from": (current_x_pos, y_start), "to": (current_x_pos, y_end)}
    )
    return lines_list


def generate_v2(bipole_tokens=BIPOLE_TOKENS, show_details=False):
    """ Generates a circuit (in the form of a ~graph) by generating a table and removing some of its lines.
        TODO
        Possible improvement : merge lines that are not cut
        Generate the inner lines first and delete some of them
        Generate the outer lines second and keep them
    """
    # generate the number of lines
    nb_vert_segments, nb_horiz_segments = np.random.randint(2, 5, size=2)

    # generate spaces between points
    nb_horiz_spaces = np.random.randint(2, 4, size=nb_vert_segments-1)
    nb_vert_spaces = np.random.randint(2, 4, size=nb_horiz_segments-1)
    if show_details:
        print("spaces", nb_horiz_spaces, nb_vert_spaces)

    # first : horizontal lines
    lines_list = []
    current_y_pos = 0
    for y_space in nb_vert_spaces:
        start_y = current_y_pos
        end_y = current_y_pos + y_space
        current_y_pos = end_y

        h_lines = get_horizontal_lines(start_y, nb_horiz_spaces)
        lines_list.extend(h_lines)

        v_lines = get_vertical_lines(start_y, end_y, nb_horiz_spaces)
        lines_list.extend(v_lines)

    # add last horizontal line
    h_lines = get_horizontal_lines(current_y_pos, nb_horiz_spaces)
    lines_list.extend(h_lines)

    # delete randomly some segments
    nb_to_delete = np.random.randint(0, len(lines_list)//3)
    lines_to_delete = np.random.randint(0, len(lines_list), size=nb_to_delete)
    lines_list = [lines_list[i]
                  for i in range(len(lines_list)) if i not in lines_to_delete]
    if show_details:
        print(f"Deleted {nb_to_delete} segments")

    # add some bipoles (and some labels)
    for line in lines_list:
        # important probability of getting a line
        if np.random.rand() < 0.3:
            line["type"] = "short"
        elif np.random.rand() < 0.2:
            line["type"] = "open"
        else:
            line["type"] = np.random.choice(bipole_tokens)

        # add a few labels
        if np.random.rand() < 0.3:
            line["label"] = f"$R_{np.random.randint(0, 9)}$"

    return lines_list


def display_circuit(segments_list, save=False):
    """Displays the circuit in a readable way"""
    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'
    for element in segments_list:
        plt.plot([element["from"][0], element["to"][0]],
                 [element["from"][1], element["to"][1]], '-o')
    if save:
        plt.savefig("circuit_generation_0.png", dpi=300)
    plt.show()


# tests
if __name__ == "__main__":
    # segments_list = generate_one_loop_circuit()
    segments_list = generate_v2()
    # print(segments_list)
    display_circuit(segments_list)
