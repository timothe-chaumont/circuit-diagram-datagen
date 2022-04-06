import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from typing import List, Tuple, Union, Set, Optional
from typing_extensions import Literal

# later : use objects instead of dictionnaries

BIPOLE_TOKENS = ["short", "open", "generic",
                 "capacitor", "cute inductor",
                 "battery1", "european voltage source", "european current source",
                 "ammeter", "voltmeter",
                 "normal open switch"]


class Segment:
    def __init__(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], element: str = None, label: str = None) -> None:
        """
        Args:
            from_pos (Tuple[int, int]): the coordinates of the before node
            to_pos (Tuple[int, int]): the coordinates of the after node
            element (str, optional): the kind of electrical element (can be a wire). Defaults to None.
            label (str, optional): an optional label for the element. Defaults to None.
        """
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.type = element
        self.label = label

    def set_type(self, element: str):
        if self.type is None:
            self.type = element
        raise Exception("Segment already has a type")

    def __repr__(self) -> str:
        if self.type:
            return f"{self.from_pos}-{self.type}-{self.to_pos}"
        else:
            return f"{self.from_pos}-{self.to_pos}"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Segment):
            return self.from_pos == __o.from_pos and self.to_pos == __o.to_pos and self.type == __o.type
        return False

    def __hash__(self):
        return hash(str(self))


class CircuitGenerator:
    def __init__(self, p_label: float = 0.1) -> None:
        """Choose probabilities for various aspects of the circuits we generate.

            Args:
                p_label (float): probability of a segment having a label.
        """
        self.p_label: float = p_label
        self.segments: Set[Segment] = set()

    def get_line_segments(self, segments_lengths: List[int], orientation: Union[Literal["horizontal"], Literal["vertical"]], offset: int, init_pos: int = 0) -> Set[Segment]:
        """Returns a list of adjacent segments of given length, from a position, 

        Args:
            segments_lengths (List[int]): List of lengths of the segments to return
            orientation ("horizontal" | "vertical"): Orientation of the returned segments
            offset (int): Offset of the segments to return. If 
            init_pos (int): Initial start position of the segments, along the axis of the segments (z if vertical, ...)
        """
        segments: Set[Segment] = set()

        start_pos: int = init_pos
        for length in segments_lengths:
            if orientation == "horizontal":
                x_start, x_end = start_pos, start_pos + length
                y_start, y_end = offset, offset
            # vertical
            else:
                x_start, x_end = offset, offset
                y_start, y_end = start_pos, start_pos + length
            segments.add(
                Segment((x_start, y_start), (x_end, y_end))
            )
            start_pos += length
        return segments

    def get_inside_segments(self, nb_vert_lines: int, nb_horiz_lines: int, nb_horiz_spaces: List[int], nb_vert_spaces: List[int]) -> Set[Segment]:
        """Returns all the segments of the initial grid except the outline.
           The upper left of the grid is at position (0, 0)

           Args:
                nb_vert_lines (int): Total number of vertical lines (composed of multiple segments) in the initial grid
                nb_horiz_lines (int): Total number of horizontal lines in the initial grid
                nb_horiz_spaces (List[int]): List of spaces between vertical lines
                nb_vert_spaces (List[int]): List of spaces between horizontal lines

            Returns:
                Set[Segment]: Set of segments inside the initial 'blueprint'of the circuit.
        """
        inside_segments: Set[Segment] = set()
        # vertical lines
        offset = 0
        for vertical_line_id in range(0, nb_vert_lines-2):
            # update the offset
            offset += nb_horiz_spaces[vertical_line_id]
            # add the line segments
            inside_segments.update(
                self.get_line_segments(
                    segments_lengths=nb_vert_spaces,
                    orientation="vertical",
                    offset=offset,
                    init_pos=0
                )
            )

        # horizontal lines
        offset = 0
        for horizontal_line_id in range(0, nb_horiz_lines-2):
            # update the offset
            offset += nb_vert_spaces[horizontal_line_id]
            # add the line segments
            inside_segments.update(
                self.get_line_segments(
                    segments_lengths=nb_horiz_spaces,
                    orientation="horizontal",
                    offset=offset,
                    init_pos=0
                )
            )

        return inside_segments

    def get_outside_segments(self, nb_horiz_spaces: List[int], nb_vert_spaces: List[int]) -> Set[Segment]:
        """Returns the outline segments of the initial grid.
           The upper left of the grid is at position (0, 0)

           Args:
                nb_vert_lines (int): Total number of vertical lines (composed of multiple segments) in the initial grid
                nb_horiz_lines (int): Total number of horizontal lines in the initial grid
                nb_horiz_spaces (List[int]): List of spaces between vertical lines
                nb_vert_spaces (List[int]): List of spaces between horizontal lines

            Returns:
                Set[Segment]: Set of segments on the outline of the initial 'blueprint' of the circuit.
        """
        outside_segments: Set[Segment] = set()
        # vertical lines
        for offset in (0, sum(nb_horiz_spaces)):
            outside_segments.update(
                self.get_line_segments(
                    segments_lengths=nb_vert_spaces,
                    orientation="vertical",
                    offset=offset,
                    init_pos=0
                )
            )

        # horizontal
        for offset in (0, sum(nb_vert_spaces)):
            outside_segments.update(
                self.get_line_segments(
                    segments_lengths=nb_horiz_spaces,
                    orientation="horizontal",
                    offset=offset,
                    init_pos=0
                )
            )
        return outside_segments

    def add_elements(self) -> None:
        for segment in self.segments:
            # choose an element
            # possibly add a label, and choose its position
            # important probability of getting a line
            if np.random.rand() < 0.3:
                segment.type = "short"
            # elif np.random.rand() < 0.2:
            #     segment["type"] = "open"
            else:
                segment.type = np.random.choice(BIPOLE_TOKENS)

    def generate_one_circuit(self) -> Set[Segment]:
        """Generates a circuit in the form of a list of segments.

        Steps : 
            1. choose the number of horizontal and vertical lines.
            2. Create the inside segments of this lines grid
            3. With some probability, remove some of those lines
            4. Add the outlines
            5. Remove some of the outlines
            6. Add bipoles & labels

        Returns:
            Set[Segment]: Set of segments that define the circuit
        """
        # pick a number of lines for the initial grid
        nb_vert_lines, nb_horiz_lines = np.random.randint(2, 5, size=2)

        # draw spaces between lines of the grid (= segments lengths)
        nb_horiz_spaces: int = np.random.randint(2, 4, size=nb_vert_lines-1)
        nb_vert_spaces: int = np.random.randint(2, 4, size=nb_horiz_lines-1)

        inside_segments = self.get_inside_segments(
            nb_vert_lines, nb_horiz_lines, nb_horiz_spaces, nb_vert_spaces)

        # later: remove some of these inside segments

        outline_segments = self.get_outside_segments(
            nb_horiz_spaces, nb_vert_spaces)

        self.segments = inside_segments | outline_segments
        # add elements to all segments
        self.add_elements()

        return self.segments


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

        Returns:
          A list of dictionnaries with keys : 
          - "from" : the position of the before node
          - "to" : the position of the after node
          - "type" : the kind of electrical bipole
          - "label" : the legend of the bipole
        #   - "label_pos" : the position of the legend
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
        plt.plot([element.from_pos[0], element.to_pos[0]],
                 [element.from_pos[1], element.to_pos[1]], '-o')
    if save:
        plt.savefig("circuit_generation_0.png", dpi=300)
    plt.show()


# tests
if __name__ == "__main__":
    # segments_list = generate_one_loop_circuit()
    # segments_list = generate_v2()
    # print(segments_list)
    g = CircuitGenerator()
    segments_list = g.generate_one_circuit()
    print(segments_list)
    display_circuit(segments_list)
