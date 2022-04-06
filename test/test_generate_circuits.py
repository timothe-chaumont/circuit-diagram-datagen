from scripts.data_generation.generate_circuits import Segment, CircuitGenerator


class TestGetSegments:
    generator = CircuitGenerator()

    def test_get_vertical_segments(self):
        segments_Lengths = [2, 3]
        orientation = "vertical"
        offset = 2
        init_pos = 0
        segments = self.generator.get_line_segments(
            segments_Lengths, orientation, offset, init_pos)

        expected_segments = {
            Segment((offset, 0), (offset, 2)),
            Segment((offset, 2), (offset, 5)),
        }
        assert segments == expected_segments

    def test_get_horizontal_segments(self):
        segments_Lengths = [2, ]
        orientation = "horizontal"
        offset = 0
        init_pos = 5
        segments = self.generator.get_line_segments(
            segments_Lengths, orientation, offset, init_pos)

        expected_segments = {
            Segment((5, offset), (7, offset))
        }
        assert segments == expected_segments


class TestGetInsideSegments:
    generator = CircuitGenerator()

    def test_no_segements(self):
        """A circuit with 2 segments h & v """
        inside_segments = self.generator.get_inside_segments(
            2, 2, [3, ], [4, ]
        )
        assert inside_segments == set()

    def test_one_horizontal_segment(self):
        """A circuit with 3 horizontal segments and 2 vertical ones
            Therefore, only one horizontal segment should get returned.
        """
        nb_vert_lines = 2
        nb_horiz_lines = 3
        nb_horiz_spaces = [3, ]
        nb_vert_spaces = [2, 2]

        inside_segments = self.generator.get_inside_segments(
            nb_vert_lines, nb_horiz_lines, nb_horiz_spaces, nb_vert_spaces)
        assert len(
            inside_segments) == 1, f"expected one segment, but {len(inside_segments)} were returned"

        y_pos = 0 + nb_vert_spaces[0]
        x_start = 0
        x_end = x_start + nb_horiz_spaces[0]
        expected_segment = Segment(
            (x_start, y_pos), (x_end, y_pos)
        )
        assert list(inside_segments)[0] == expected_segment

    def test_one_vertical_segment(self):
        """A circuit with 2 horizontal segments and 3 vertical ones
            Therefore, only one vertical segment should get returned.
        """
        nb_vert_lines = 3
        nb_horiz_lines = 2
        nb_horiz_spaces = [3, 2]
        nb_vert_spaces = [2, ]

        inside_segments = self.generator.get_inside_segments(
            nb_vert_lines, nb_horiz_lines, nb_horiz_spaces, nb_vert_spaces)
        assert len(
            inside_segments) == 1, f"expected one segment, but {len(inside_segments)} were returned"

        x_pos = 0 + nb_horiz_spaces[0]
        y_start = 0
        y_end = y_start + nb_vert_spaces[0]
        expected_segment = Segment(
            (x_pos, y_start), (x_pos, y_end)
        )
        assert list(inside_segments)[0] == expected_segment

    def test_two_vertical_segments(self):
        """A circuit with 2 horizontal segments and 4 vertical ones
            Therefore, 2 vertical segment should get returned.
        """
        nb_vert_lines = 4
        nb_horiz_lines = 2
        nb_horiz_spaces = [1, 1, 1]
        nb_vert_spaces = [2, ]

        inside_segments = self.generator.get_inside_segments(
            nb_vert_lines, nb_horiz_lines, nb_horiz_spaces, nb_vert_spaces)
        assert len(
            inside_segments) == 2, f"expected two segments, but {len(inside_segments)} were returned"

        expected_segments = {
            Segment((1, 0), (1, 2)),
            Segment((2, 0), (2, 2))
        }
        assert inside_segments == expected_segments

    def test_one_segment_for_each_orientation(self):
        """A circuit with 3 horizontal segments and 3 vertical ones
            Therefore, one horizontal and one vertical segments should get returned.
        """
        nb_vert_lines = 3
        nb_horiz_lines = 3
        nb_horiz_spaces = [1, 1]
        nb_vert_spaces = [4, 4]

        generated_segments = self.generator.get_inside_segments(
            nb_vert_lines, nb_horiz_lines, nb_horiz_spaces, nb_vert_spaces)
        assert len(
            generated_segments) == 4, f"expected four segment , but {len(generated_segments)} were returned"

        # we use sets to avoid seeing ordering errors
        horizontal_segments = {
            Segment((0, 4), (1, 4)), Segment((1, 4), (2, 4))
        }
        vertical_segments = {
            Segment((1, 0), (1, 4)), Segment((1, 4), (1, 8))
        }
        expected_segments = set(vertical_segments | horizontal_segments)
        assert generated_segments == expected_segments


class TestGetOutlineSegments:
    generator = CircuitGenerator()

    def test_no_inside_segements(self):
        """A circuit with 2 horizontal and vertical segments """
        inside_segments = self.generator.get_outside_segments(
            [3, ], [4, ]
        )
        expected_segments = {
            Segment((0, 0), (3, 0)),  Segment((0, 4), (3, 4)),  # horizontal
            Segment((0, 0), (0, 4)), Segment((3, 0), (3, 4))  # vertical
        }
        assert inside_segments == expected_segments

    def test_two_inside_segements(self):
        """A circuit with 3 horizontal and vertical segments """
        inside_segments = self.generator.get_outside_segments(
            [1, 1], [1, 1]
        )
        expected_segments = {
            # horizontal
            Segment((0, 0), (1, 0)),  Segment((1, 0), (2, 0)),
            Segment((0, 2), (1, 2)), Segment((1, 2), (2, 2)),
            # vertical
            Segment((0, 0), (0, 1)), Segment((0, 1), (0, 2)),
            Segment((2, 0), (2, 1)), Segment((2, 1), (2, 2))
        }
        assert inside_segments == expected_segments
