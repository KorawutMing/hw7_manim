from manim import *
import numpy as np

class SimplexPath3D(ThreeDScene):
    def construct(self):
        # --- 1. CONFIGURATION AND SETUP ---
        
        # Setup camera angle with zoom to fit polyhedron
        self.set_camera_orientation(phi=70*DEGREES, theta=40*DEGREES, zoom=0.6)
        self.begin_ambient_camera_rotation(rate=0.08)

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[0, 12, 2],
            y_range=[0, 12, 2],
            z_range=[0, 12, 2],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        
        # Add axis labels with proper math mode
        x_label = axes.get_x_axis_label(Tex("$x_{1}$"))
        y_label = axes.get_y_axis_label(Tex("$x_{2}$")).shift(UP * 0.5)
        z_label = axes.get_z_axis_label(Tex("$x_{3}$"))
        
        # Display axes
        self.play(Create(axes), run_time=1.5)
        self.add(x_label, y_label, z_label)
        
        # Define vertices in 3D coordinates
        A_coord = (0, 0, 0)
        D_coord = (10, 0, 0)
        B_coord = (0, 0, 10)
        C_coord = (0, 10, 0)
        E_coord = (4, 4, 4)

        A = axes.coords_to_point(*A_coord)
        B = axes.coords_to_point(*B_coord)
        C = axes.coords_to_point(*C_coord)
        D = axes.coords_to_point(*D_coord)
        E = axes.coords_to_point(*E_coord)
        
        # ===== PHASE 1: RENDER FACES AND EDGES =====
        
        # Define faces of the polyhedron
        FILL_OPACITY = 0.15
        
        faces_data = [
            ([A, C, D], BLUE_A),
            ([A, B, C], BLUE_B),
            ([A, D, B], BLUE_C),
            ([D, C, E], TEAL_A),
            ([C, B, E], TEAL_B),
            ([B, D, E], TEAL_C),
        ]
        
        faces = []
        for vertices, color in faces_data:
            face = Polygon(
                *vertices,
                fill_color=color,
                fill_opacity=FILL_OPACITY,
                stroke_width=0,
                shade_in_3d=True
            )
            faces.append(face)
        
        # Display faces first for depth sorting
        self.play(*[Create(face) for face in faces], run_time=1.5)
        
        # Draw polyhedron edges
        edges = VGroup(
            Line3D(start=A, end=B, color=GRAY, thickness=0.015),
            Line3D(start=A, end=C, color=GRAY, thickness=0.015),
            Line3D(start=A, end=D, color=GRAY, thickness=0.015),
            Line3D(start=B, end=E, color=GRAY, thickness=0.015),
            Line3D(start=C, end=E, color=GRAY, thickness=0.015),
            Line3D(start=D, end=E, color=GRAY, thickness=0.015),
        )
        self.play(Create(edges), run_time=1.5)

        # Create dots and labels for vertices
        dot_A = Dot3D(point=A, color=WHITE, radius=0.1)
        dot_B = Dot3D(point=B, color=WHITE, radius=0.1)
        dot_C = Dot3D(point=C, color=WHITE, radius=0.1)
        dot_D = Dot3D(point=D, color=WHITE, radius=0.1)
        dot_E = Dot3D(point=E, color=YELLOW, radius=0.12)
        
        # Create labels that follow the 3D points
        label_A = always_redraw(lambda: Text("A(0,0,0)", font_size=18).next_to(dot_A, DOWN + LEFT, buff=0.1))
        label_B = always_redraw(lambda: Text("B(0,0,10)", font_size=18).next_to(dot_B, UP, buff=0.1))
        label_C = always_redraw(lambda: Text("C(0,10,0)", font_size=18).next_to(dot_C, LEFT, buff=0.1))
        label_D = always_redraw(lambda: Text("D(10,0,0)", font_size=18).next_to(dot_D, RIGHT, buff=0.1))
        label_E = always_redraw(lambda: Text("E(4,4,4)", font_size=18, color=YELLOW).next_to(dot_E, RIGHT + UP, buff=0.1))

        self.play(
            *[Create(dot) for dot in [dot_A, dot_B, dot_C, dot_D, dot_E]],
            run_time=1
        )
        self.add(label_A, label_B, label_C, label_D, label_E)
        self.play(
            *[Write(label) for label in [label_A, label_B, label_C, label_D, label_E]],
            run_time=1
        )
        
        # Display objective function
        obj_func = MathTex(
            r"\text{Minimize: } Z = -10x_1 - 12x_2 - 12x_3",
            font_size=28
        ).to_corner(UL).shift(DOWN * 0.2)
        self.add_fixed_in_frame_mobjects(obj_func)
        self.play(Write(obj_func), run_time=1)
        self.wait(1)
        
        # ===== PHASE 2: SIMPLEX PATH WITH FULL TABLEAUX =====
        
        # Full Simplex tableau data with complete matrices
        tableau_data = {
            0: {  # Vertex A
                "matrix": [
                    [r"20", r"0", r"1", r"2", r"2", r"1", r"0", r"0"],
                    [r"20", r"0", r"2", r"1", r"2", r"0", r"1", r"0"],
                    [r"20", r"0", r"2", r"2", r"1", r"0", r"0", r"1"]
                ],
                "basis": [r"s_1", r"s_2", r"s_3"],
                "z_val": r"0"
            },
            1: {  # Vertex D
                "matrix": [
                    [r"10", r"0", r"0", r"3/2", r"1/2", r"1", r"{-1/2}", r"0"],
                    [r"10", r"0", r"1", r"1/2", r"1", r"0", r"1/2", r"0"],
                    [r"0", r"0", r"0", r"1", r"{-1}", r"0", r"{-1}", r"1"]
                ],
                "basis": [r"s_1", r"x_1", r"s_3"],
                "z_val": r"{-100}"
            },
            2: {  # Vertex B
                "matrix": [
                    [r"10", r"0", r"0", r"3/2", r"1/2", r"1", r"{-1/2}", r"0"],
                    [r"10", r"0", r"1", r"1/2", r"1", r"0", r"1/2", r"0"],
                    [r"0", r"0", r"0", r"1", r"{-1}", r"0", r"{-1}", r"1"]
                ],
                "basis": [r"s_1", r"x_3", r"s_3"],
                "z_val": r"{-120}"
            },
            3: {  # Vertex C
                "matrix": [
                    [r"10", r"0", r"0", r"1", r"0", r"1", r"{-1}", r"0"],
                    [r"10", r"0", r"1", r"0", r"1", r"0", r"1/2", r"0"],
                    [r"0", r"0", r"0", r"0", r"0", r"0", r"0", r"1"]
                ],
                "basis": [r"x_2", r"x_1", r"s_3"],
                "z_val": r"{-120}"
            },
            4: {  # Vertex E (Optimal)
                "matrix": [
                    [r"4", r"0", r"0", r"0", r"1", r"3/5", r"2/5", r"{-2/5}"],
                    [r"4", r"0", r"1", r"0", r"0", r"{-2/5}", r"3/5", r"{-1/5}"],
                    [r"4", r"0", r"0", r"1", r"0", r"{-1/5}", r"{-1/5}", r"3/5"]
                ],
                "basis": [r"x_3", r"x_1", r"x_2"],
                "z_val": r"{-136}"
            }
        }
        
        # Path: A → D → B → C → E
        path_data = [
            (A, D, "D(10, 0, 0)", 1),
            (D, B, "B(0, 0, 10)", 2),
            (B, C, "C(0, 10, 0)", 3),
            (C, E, "E(4, 4, 4)", 4),
        ]
        
        # Start Tableau (Vertex A)
        initial_data = tableau_data[0]
        current_tableau = self.create_tableau(
            initial_data["matrix"],
            initial_data["basis"],
            initial_data["z_val"],
            is_optimal=False
        ).scale(0.55).to_corner(DR).shift(UP * 0.3 + LEFT * 0.2)
        
        initial_vertex_text = Text("Starting Vertex: A(0, 0, 0)", font_size=24, color=YELLOW).to_edge(UP).shift(DOWN * 0.5)
        
        self.add_fixed_in_frame_mobjects(current_tableau, initial_vertex_text)
        self.play(FadeIn(current_tableau, shift=UP), Write(initial_vertex_text), run_time=1)
        self.wait(1)
        self.remove(initial_vertex_text)

        # Main Simplex loop
        for i, (start, end, vertex_label, tableau_idx) in enumerate(path_data):
            
            data = tableau_data[tableau_idx]
            new_tableau = self.create_tableau(
                data["matrix"],
                data["basis"],
                data["z_val"],
                is_optimal=(tableau_idx == 4)
            ).scale(0.55).to_corner(DR).shift(UP * 0.3 + LEFT * 0.2)
            
            # Current vertex text
            current_vertex_text = Text(
                f"Pivot to Vertex: {vertex_label}",
                font_size=24,
                color=RED,
                weight=BOLD
            ).to_edge(UP).shift(DOWN * 0.5)

            # Create arrow for movement
            path_arrow = Arrow3D(
                start=start,
                end=end,
                color=RED,
                thickness=0.025,
                height=0.4,
                base_radius=0.1
            )
            
            self.add_fixed_in_frame_mobjects(current_vertex_text)
            
            # Animate arrow and tableau transformation
            self.play(
                Create(path_arrow),
                Transform(current_tableau, new_tableau),
                Write(current_vertex_text),
                run_time=2
            )
            self.wait(1)

            # Clean up for next iteration
            if i < 3:
                self.play(FadeOut(current_vertex_text), run_time=0.5)
            else:
                self.remove(current_vertex_text)
        
        # ===== OPTIMAL SOLUTION HIGHLIGHT =====
        self.stop_ambient_camera_rotation()
        
        # Final highlight
        self.play(
            Flash(dot_E, color=GOLD, line_length=0.4, num_lines=16, flash_radius=0.6),
            dot_E.animate.scale(1.5).set_color(GOLD),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Display optimal solution banner
        optimal_banner = VGroup(
            Text(
                "OPTIMAL SOLUTION FOUND!",
                font_size=32,
                color=GOLD,
                weight=BOLD
            ),
            MathTex(
                r"x_1 = 4, \quad x_2 = 4, \quad x_3 = 4",
                font_size=26,
                color=YELLOW
            ),
            MathTex(
                r"Z_{\text{min}} = -136",
                font_size=28,
                color=GREEN_E
            )
        ).arrange(DOWN, buff=0.3).to_corner(UL).shift(DOWN * 1.5)
        
        self.add_fixed_in_frame_mobjects(optimal_banner)
        self.play(Write(optimal_banner), run_time=2)
        
        # Final rotation
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(2)
    
    def create_tableau(self, matrix_data, basis_labels, z_val, is_optimal=False):
        """Create a full Simplex tableau display with 4 rows and 8 columns"""
        
        # Header row: RHS, Z, x1, x2, x3, s1, s2, s3
        header = [r"\text{RHS}", r"\text{Z}", r"x_1", r"x_2", r"x_3", r"s_1", r"s_2", r"s_3"]
        
        # Combine header with matrix data
        table_data = [header] + matrix_data
        
        # Create table with proper sizing
        table = MathTable(
            table_data,
            include_outer_lines=True,
            h_buff=0.25,
            v_buff=0.25,
            element_to_mobject=lambda t: MathTex(t, font_size=16)
        )
        
        # Add basis labels to the left of each data row
        basis_group = VGroup()
        for i, basis_var in enumerate(basis_labels):
            label = MathTex(basis_var, font_size=16, color=YELLOW)
            # Position labels to the left of each data row (skip header row)
            row_position = table.get_rows()[i + 1].get_left()
            label.next_to(row_position, LEFT, buff=0.3)
            basis_group.add(label)
        
        # Create Z-value display
        z_display = MathTex(
            f"Z = {z_val}",
            font_size=20,
            color=GREEN if is_optimal else BLUE
        ).next_to(table, DOWN, buff=0.3)
        
        # Title
        title = Text(
            "Simplex Tableau" if not is_optimal else "OPTIMAL TABLEAU",
            font_size=20,
            weight=BOLD,
            color=GOLD if is_optimal else BLUE_B
        )
        
        # Arrange all components
        tableau_content = VGroup(title, table, basis_group, z_display).arrange(DOWN, buff=0.25)
        
        # Add background rectangle
        bg_rect = SurroundingRectangle(
            tableau_content,
            color=GOLD if is_optimal else BLUE,
            fill_opacity=0.15,
            stroke_width=3 if is_optimal else 2,
            buff=0.25
        )
        
        return VGroup(bg_rect, tableau_content)