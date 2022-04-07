import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from typing import List, Set, Dict, Tuple, Union, Optional
from typing_extensions import Literal

# later : use objects instead of dictionnaries

BIPOLE_TOKENS: List[str] = ["generic",
                            "capacitor", "cute inductor",
                            "normal open switch"]

SOURCES_BIPOLES: List[str] = ["battery1",
                              "european voltage source", "european current source"]

MEASURE_BIPOLES: List[str] = ["ammeter", "voltmeter"]


class Bipole:
    def __init__(self, name: str, legends: List[str]) -> None:
        self.name: str = name
        self.legends: List[str] = legends

    def __str__(self) -> str:
        self.name


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
    def __init__(self, p_remove_inside_segment: float = 0.1, p_remove_outline_segment: float = 0.05,
                 p_line: float = 0.4, p_source: float = 0.1, p_measure: float = 0.1, p_label: float = 0.5) -> None:
        """Choose probabilities for various aspects of the circuits we generate.

            Args:
                p_line (float): probability of having a line instaed of a bipole
                p_remove_inside_segment (float): probability of removing a segment inside the circuit
                p_label (float): probability of a bipole to have a label.
        """
        # set probabilitites
        # of removing segmentsfrom the initial grid
        self.p_remove_inside_segment: float = p_remove_inside_segment
        self.p_remove_outline_segment: float = p_remove_outline_segment
        # of placing various types of bipoles
        self.p_line: float = p_line
        self.p_source: float = p_source
        self.p_measure: float = p_measure
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

    def add_bipoles(self) -> None:
        """Add bipoles with a certain probability for each class.
           Later : add labels and indications to the bipoles.
        """
        for segment in self.segments:
            # choose an element
            rand_nb = np.random.rand()
            # possibly add a label, and choose its position
            if rand_nb < self.p_line:
                segment.type = "short"
            # with some probability, add a source
            elif rand_nb < self.p_line + self.p_source:
                segment.type = np.random.choice(SOURCES_BIPOLES)
            elif rand_nb < self.p_line + self.p_source + self.p_measure:
                segment.type = np.random.choice(MEASURE_BIPOLES)
            else:
                segment.type = np.random.choice(BIPOLE_TOKENS)
                # possibly add a label

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

        # remove some of these inside segments
        for segment in tuple(inside_segments):
            if np.random.rand() < self.p_remove_inside_segment:
                inside_segments.remove(segment)

        outline_segments = self.get_outside_segments(
            nb_horiz_spaces, nb_vert_spaces)

        # remove a few outline segments
        for segment in tuple(outline_segments):
            if np.random.rand() < self.p_remove_outline_segment:
                outline_segments.remove(segment)

        self.segments = inside_segments | outline_segments
        # add elements to all segments
        self.add_bipoles()

        return self.segments


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
