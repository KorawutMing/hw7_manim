from manim import *
import numpy as np

class SimplexPath3D(ThreeDScene):
    def construct(self):
        # --- 1. CONFIGURATION AND SETUP ---
        
        # Setup camera angle with zoom to fit polyhedron
        self.set_camera_orientation(phi=70*DEGREES, theta=40*DEGREES, zoom=0.65)
        self.begin_ambient_camera_rotation(rate=0.08)

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[0, 12, 2],
            y_range=[0, 12, 2],
            z_range=[0, 12, 2],
            x_length=5.5,
            y_length=5.5,
            z_length=5.5,
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
            font_size=22
        ).to_corner(UL).shift(DOWN * 0.1 + RIGHT * 0.2)
        self.add_fixed_in_frame_mobjects(obj_func)
        self.play(Write(obj_func), run_time=1)
        self.wait(1)
        
        # ===== PHASE 2: SIMPLEX PATH WITH CORRECTED TABLEAUX =====
        
        # Corrected Simplex tableau data (7 columns: Z-row values, then 3 constraint rows)
        # Using simpler fraction notation that renders properly
        tableau_data = {
            0: {  # Vertex A
                "matrix": [
                    ["--", "10", "12", "12", "0", "0", "0"],
                    ["20", "1", "2", "2", "1", "0", "0"],
                    ["20", "2", "1", "2", "0", "1", "0"],
                    ["20", "2", "2", "1", "0", "0", "1"]
                ],
                "basis": ["Z", "x_4", "x_5", "x_6"],
                "z_val": "0",
                "solution": "[0, 0, 0]"
            },
            1: {  # Vertex D
                "matrix": [
                    ["--", "0", "7", "2", "0", "-5", "0"],
                    ["10", "0", "3/2", "1", "1", "-1/2", "0"],
                    ["10", "1", "1/2", "1", "0", "1/2", "0"],
                    ["0", "0", "1", "-1", "0", "-1", "1"]
                ],
                "basis": ["Z", "x_4", "x_1", "x_6"],
                "z_val": "-100",
                "solution": "[10, 0, 0]"
            },
            2: {  # Vertex B
                "matrix": [
                    ["--", "0", "4", "0", "-2", "-4", "0"],
                    ["10", "0", "3/2", "1", "1", "-1/2", "0"],
                    ["0", "1", "-1", "0", "-1", "1", "0"],
                    ["10", "0", "5/2", "0", "1", "-3/2", "1"]
                ],
                "basis": ["Z", "x_3", "x_1", "x_6"],
                "z_val": "-120",
                "solution": "[0, 0, 10]"
            },
            3: {  # Vertex E (Optimal)
                "matrix": [
                    ["--", "0", "0", "0", "-18/5", "-8/5", "-8/5"],
                    ["4", "0", "0", "1", "2/5", "2/5", "-3/5"],
                    ["4", "1", "0", "0", "-3/5", "2/5", "2/5"],
                    ["4", "0", "1", "0", "2/5", "-3/5", "2/5"]
                ],
                "basis": ["Z", "x_3", "x_1", "x_2"],
                "z_val": "-136",
                "solution": "[4, 4, 4]"
            }
        }
        z_values = [int(tableau_data[key]["z_val"]) for key in tableau_data]
        
        # Path: A → D → B → E (Note: Path changed based on provided data)
        path_data = [
            (A, D, "D(10, 0, 0)", 1),
            (D, B, "B(0, 0, 10)", 2),
            (B, E, "E(4, 4, 4)", 3),
        ]
        
        # Start Tableau (Vertex A)
        initial_data = tableau_data[0]
        current_tableau = self.create_tableau(
            initial_data["matrix"],
            initial_data["basis"],
            initial_data["z_val"],
            initial_data["solution"],
            is_optimal=False
        ).scale(0.68).to_corner(UR).shift(DOWN * 1.0 + LEFT * 0.3)
        
        initial_vertex_text = Text("Starting Vertex: A(0, 0, 0)", font_size=20, color=YELLOW).to_edge(DOWN).shift(UP * 0.3)
        
        self.add_fixed_in_frame_mobjects(current_tableau, initial_vertex_text)
        self.play(FadeIn(current_tableau, shift=UP), Write(initial_vertex_text), run_time=1)
        self.wait(1)
        self.remove(initial_vertex_text)

        # Main Simplex loop
        for i, (start, end, vertex_label, tableau_idx) in enumerate(path_data):
            
            data = tableau_data[tableau_idx]
            
            # 1. Create the NEW tableau object
            new_tableau = self.create_tableau(
                # Ensure you are still using the fraction formatting helper here!
                data["matrix"],
                data["basis"],
                data["z_val"],
                data["solution"],
                is_optimal=(tableau_idx == 3)
            ).scale(0.68).to_corner(UR).shift(DOWN * 1.0 + LEFT * 0.3)
            
            # 2. Add the NEW tableau to the fixed list immediately.
            # This registers it as screen-space, but it's currently invisible.
            self.add_fixed_in_frame_mobjects(new_tableau)

            # Current vertex text... (rest of setup)
            current_vertex_text = Text(
                f"Pivot to: {vertex_label}",
                font_size=20,
                color=RED,
                weight=BOLD
            ).to_edge(DOWN).shift(UP * 0.3)
            self.add_fixed_in_frame_mobjects(current_vertex_text)

            # Create arrow for movement
            path_arrow = Arrow3D(start=start, end=end, color=RED, thickness=0.025, height=0.4, base_radius=0.1)
            
            # 3. Animate the path AND the table cross-fade
            self.play(
                Create(path_arrow),
                # FIXED: Fade out the old one and fade in the new one.
                # This ensures the new one stays fixed to the frame.
                FadeOut(current_tableau),
                FadeIn(new_tableau),
                Write(current_vertex_text),
                run_time=2
            )
            self.wait(1)

            # 4. IMPORTANT: Update the reference for the next loop
            current_tableau = new_tableau

            # Clean up for next iteration
            if i < len(path_data) - 1:
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
                font_size=26,
                color=GOLD,
                weight=BOLD
            ),
            MathTex(
                r"x_1 = 4, \quad x_2 = 4, \quad x_3 = 4",
                font_size=22,
                color=YELLOW
            ),
            MathTex(
                r"Z_{\text{min}} = -136",
                font_size=24,
                color=GREEN_E
            )
        ).arrange(DOWN, buff=0.25).to_edge(LEFT).shift(UP * 2 + RIGHT * 0.5)
        
        self.add_fixed_in_frame_mobjects(optimal_banner)
        self.play(Write(optimal_banner), run_time=2)
        
        # Final rotation
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(2)
    
    def create_tableau(self, matrix_data, basis_labels, z_val, solution, is_optimal=False):
        """Create a full Simplex tableau display using MobjectTable"""
        
        # Header row: RHS, x1, x2, x3, x4, x5, x6
        headers = [
            Text("RHS", font_size=16, color=BLUE_B, weight=BOLD),
            Text("x₁", font_size=16, color=BLUE_B, weight=BOLD),
            Text("x₂", font_size=16, color=BLUE_B, weight=BOLD),
            Text("x₃", font_size=16, color=BLUE_B, weight=BOLD),
            Text("x₄", font_size=16, color=BLUE_B, weight=BOLD),
            Text("x₅", font_size=16, color=BLUE_B, weight=BOLD),
            Text("x₆", font_size=16, color=BLUE_B, weight=BOLD)
        ]
        
        # Create data cells as Text objects
        data_cells = []
        for row_data in matrix_data:
            row = [MathTex(str(cell), font_size=16) for cell in row_data]
            data_cells.append(row)
        
        # Combine header and data
        all_cells = [headers] + data_cells
        
        # Create MobjectTable
        table = MobjectTable(
            all_cells,
            include_outer_lines=True,
            h_buff=0.6,
            v_buff=0.3,
            line_config={"stroke_width": 2, "color": WHITE}
        )
        print(table)
        
        # Title
        title = Text(
            "Simplex Tableau" if not is_optimal else "OPTIMAL TABLEAU",
            font_size=20,
            weight=BOLD,
            color=GOLD if is_optimal else BLUE_B
        )
        
        # Arrange all components
        tableau_content = VGroup(title, table).arrange(DOWN, buff=0.3)
        
        # Add background rectangle
        bg_rect = SurroundingRectangle(
            tableau_content,
            color=GOLD if is_optimal else BLUE,
            fill_opacity=0.15,
            stroke_width=3 if is_optimal else 2,
            buff=0.28
        )
        
        return VGroup(bg_rect, tableau_content)
    
    def create_z_chart(self, z_values):
        """Creates a static graph frame for Z-value tracking."""
        # Setup axes
        axes = Axes(
            x_range=[0, len(z_values) - 1, 1],
            y_range=[-140, 10, 20], # Range encompassing 0 to -136
            x_length=4.5,
            y_length=2.5,
            axis_config={"include_numbers": True, "font_size": 18}
        ).to_corner(DL).shift(UP * 0.3)
        
        # Labels
        x_label = axes.get_x_axis_label(Tex(r"\text{Iteration}"))
        y_label = axes.get_y_axis_label(Tex(r"Z\text{-Value}")).rotate(90 * DEGREES)
        
        # Chart Title
        chart_title = Text("Objective Function Value (Z)", font_size=20).next_to(axes, UP, buff=0.2)
        
        chart_group = VGroup(axes, x_label, y_label, chart_title)
        
        # Add background rectangle
        bg_rect = SurroundingRectangle(
            chart_group,
            color=GRAY_A,
            fill_opacity=0.15,
            stroke_width=1.5,
            buff=0.3
        )
        
        return VGroup(bg_rect, chart_group)