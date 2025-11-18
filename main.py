from manim import *
import numpy as np

class SimplexPath3D(ThreeDScene):
    def construct(self):
        # --- 1. CONFIGURATION AND SETUP ---
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[0, 12, 2],
            y_range=[0, 12, 2],
            z_range=[0, 12, 2],
            x_length=5.5,
            y_length=5.5,
            z_length=5.5,
        )

        # Define vertices
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

        # --- CAMERA OFFSET LOGIC (FIXED) ---
        # 1. Define the constant OFFSET (How far to shift camera view)
        # Looking UP (OUT) and RIGHT makes the object appear DOWN and LEFT.
        CAMERA_OFFSET = 3.5 * OUT + 5.0 * RIGHT
        
        # 2. Define the initial GEOMETRIC focus (Where the object actually is)
        centroid_coords = np.mean([A_coord, B_coord, C_coord, D_coord, E_coord], axis=0)
        geo_focus_point = axes.coords_to_point(*centroid_coords)

        # 3. Apply: Target = Geometry + Offset
        self.set_camera_orientation(
            phi=70*DEGREES, 
            theta=40*DEGREES, 
            zoom=0.6, 
            frame_center=geo_focus_point + CAMERA_OFFSET
        )
        self.begin_ambient_camera_rotation(rate=0.08)

        # Add labels and display axes
        x_label = axes.get_x_axis_label(Tex("$x_{1}$"))
        y_label = axes.get_y_axis_label(Tex("$x_{2}$")).shift(UP * 0.5)
        z_label = axes.get_z_axis_label(Tex("$x_{3}$"))
        
        self.play(Create(axes), run_time=1.5)
        self.add(x_label, y_label, z_label)
        
        # ===== PHASE 1: RENDER FACES AND EDGES =====
        FILL_OPACITY = 0.15
        faces_data = [
            ([A, C, D], BLUE_A), ([A, B, C], BLUE_B), ([A, D, B], BLUE_C),
            ([D, C, E], TEAL_A), ([C, B, E], TEAL_B), ([B, D, E], TEAL_C),
        ]
        
        faces = []
        for vertices, color in faces_data:
            face = Polygon(*vertices, fill_color=color, fill_opacity=FILL_OPACITY, stroke_width=0, shade_in_3d=True)
            faces.append(face)
        
        self.play(*[Create(face) for face in faces], run_time=1.5)
        
        edges = VGroup(
            Line3D(start=A, end=B, color=GRAY, thickness=0.015),
            Line3D(start=A, end=C, color=GRAY, thickness=0.015),
            Line3D(start=A, end=D, color=GRAY, thickness=0.015),
            Line3D(start=B, end=E, color=GRAY, thickness=0.015),
            Line3D(start=C, end=E, color=GRAY, thickness=0.015),
            Line3D(start=D, end=E, color=GRAY, thickness=0.015),
        )
        self.play(Create(edges), run_time=1.5)

        # Vertices and Labels
        dot_A = Dot3D(point=A, color=WHITE, radius=0.1)
        dot_B = Dot3D(point=B, color=WHITE, radius=0.1)
        dot_C = Dot3D(point=C, color=WHITE, radius=0.1)
        dot_D = Dot3D(point=D, color=WHITE, radius=0.1)
        dot_E = Dot3D(point=E, color=YELLOW, radius=0.12)
        
        label_A = always_redraw(lambda: Text("A(0,0,0)", font_size=18).next_to(dot_A, DOWN + LEFT, buff=0.1))
        label_B = always_redraw(lambda: Text("B(0,0,10)", font_size=18).next_to(dot_B, UP, buff=0.1))
        label_C = always_redraw(lambda: Text("C(0,10,0)", font_size=18).next_to(dot_C, LEFT, buff=0.1))
        label_D = always_redraw(lambda: Text("D(10,0,0)", font_size=18).next_to(dot_D, RIGHT, buff=0.1))
        label_E = always_redraw(lambda: Text("E(4,4,4)", font_size=18, color=YELLOW).next_to(dot_E, RIGHT + UP, buff=0.1))

        self.play(*[Create(d) for d in [dot_A, dot_B, dot_C, dot_D, dot_E]], run_time=1)
        self.add(label_A, label_B, label_C, label_D, label_E)
        self.play(*[Write(l) for l in [label_A, label_B, label_C, label_D, label_E]], run_time=1)
        
        # Objective Function
        obj_func = MathTex(r"\text{Minimize: } Z = -10x_1 - 12x_2 - 12x_3", font_size=22).to_corner(UL).shift(DOWN * 0.1 + RIGHT * 0.2)
        self.add_fixed_in_frame_mobjects(obj_func)
        self.play(Write(obj_func), run_time=1)
        self.wait(1)
        
        # ===== PHASE 2: SIMPLEX PATH =====
        tableau_data = {
            0: {"matrix": [["--", "10", "12", "12", "0", "0", "0"], ["20", "1", "2", "2", "1", "0", "0"], ["20", "2", "1", "2", "0", "1", "0"], ["20", "2", "2", "1", "0", "0", "1"]], "basis": ["Z", "x_4", "x_5", "x_6"], "z_val": "0", "solution": "[0, 0, 0]"},
            1: {"matrix": [["--", "0", "7", "2", "0", "-5", "0"], ["10", "0", "3/2", "1", "1", "-1/2", "0"], ["10", "1", "1/2", "1", "0", "1/2", "0"], ["0", "0", "1", "-1", "0", "-1", "1"]], "basis": ["Z", "x_4", "x_1", "x_6"], "z_val": "-100", "solution": "[10, 0, 0]"},
            2: {"matrix": [["--", "0", "4", "0", "-2", "-4", "0"], ["10", "0", "3/2", "1", "1", "-1/2", "0"], ["0", "1", "-1", "0", "-1", "1", "0"], ["10", "0", "5/2", "0", "1", "-3/2", "1"]], "basis": ["Z", "x_3", "x_1", "x_6"], "z_val": "-120", "solution": "[0, 0, 10]"},
            3: {"matrix": [["--", "0", "0", "0", "-18/5", "-8/5", "-8/5"], ["4", "0", "0", "1", "2/5", "2/5", "-3/5"], ["4", "1", "0", "0", "-3/5", "2/5", "2/5"], ["4", "0", "1", "0", "2/5", "-3/5", "2/5"]], "basis": ["Z", "x_3", "x_1", "x_2"], "z_val": "-136", "solution": "[4, 4, 4]"}
        }

        path_data = [
            (A, D, "D(10, 0, 0)", 1),
            (D, B, "B(0, 0, 10)", 2),
            (B, E, "E(4, 4, 4)", 3),
        ]
        
        # Initial Tableau
        initial_data = tableau_data[0]
        current_tableau = self.create_tableau(initial_data["matrix"], initial_data["basis"], initial_data["z_val"], initial_data["solution"], is_optimal=False).scale(0.68).to_corner(UR).shift(DOWN * 1.0 + LEFT * 0.3)
        
        initial_vertex_text = Text("Starting Vertex: A(0, 0, 0)", font_size=20, color=YELLOW).to_edge(DOWN).shift(UP * 0.3)
        self.add_fixed_in_frame_mobjects(current_tableau, initial_vertex_text)
        self.play(FadeIn(current_tableau, shift=UP), Write(initial_vertex_text), run_time=1)
        self.wait(1)
        self.remove(initial_vertex_text)

        # Main Simplex Loop
        for i, (start, end, vertex_label, tableau_idx) in enumerate(path_data):
            data = tableau_data[tableau_idx]
            
            # Create new tableau
            new_tableau = self.create_tableau(data["matrix"], data["basis"], data["z_val"], data["solution"], is_optimal=(tableau_idx == 3)).scale(0.68).to_corner(UR).shift(DOWN * 1.0 + LEFT * 0.3)
            self.add_fixed_in_frame_mobjects(new_tableau)

            # Text and Arrow
            current_vertex_text = Text(f"Pivot to: {vertex_label}", font_size=20, color=RED, weight=BOLD).to_edge(DOWN).shift(UP * 0.3)
            self.add_fixed_in_frame_mobjects(current_vertex_text)
            path_arrow = Arrow3D(start=start, end=end, color=RED, thickness=0.025, height=0.4, base_radius=0.1)
            
            # --- CAMERA UPDATE LOGIC ---
            # 1. Calculate new GEOMETRIC focus (halfway to new point)
            geo_focus_point = (geo_focus_point + end) / 2
            
            # 2. Add the CONSTANT offset
            # This ensures the "Down/Left" screen position is maintained perfectly
            target_camera_center = geo_focus_point + CAMERA_OFFSET

            # 3. Use move_camera with added_anims (Fixes the Crash)
            self.move_camera(
                frame_center=target_camera_center,
                added_anims=[
                    Create(path_arrow),
                    FadeOut(current_tableau),
                    FadeIn(new_tableau),
                    Write(current_vertex_text)
                ],
                run_time=2
            )
            
            self.wait(1)
            current_tableau = new_tableau

            if i < len(path_data) - 1:
                self.play(FadeOut(current_vertex_text), run_time=0.5)
            else:
                self.remove(current_vertex_text)
        
        # ===== OPTIMAL SOLUTION =====
        self.stop_ambient_camera_rotation()
        self.play(Flash(dot_E, color=GOLD, line_length=0.4, num_lines=16, flash_radius=0.6), dot_E.animate.scale(1.5).set_color(GOLD), run_time=1.5)
        self.wait(0.5)
        
        # optimal_banner = VGroup(
        #     Text("OPTIMAL SOLUTION FOUND!", font_size=26, color=GOLD, weight=BOLD),
        #     MathTex(r"x_1 = 4, \quad x_2 = 4, \quad x_3 = 4", font_size=22, color=YELLOW),
        #     MathTex(r"Z_{\text{min}} = -136", font_size=24, color=GREEN_E)
        # ).arrange(DOWN, buff=0.25).to_edge(LEFT).shift(UP * 2 + RIGHT * 0.5)
        
        # self.add_fixed_in_frame_mobjects(optimal_banner)
        # self.play(Write(optimal_banner), run_time=2)
        
        # Final Focus
        # self.move_camera(frame_center=E, zoom=0.7, run_time=2)
        # self.begin_ambient_camera_rotation(rate=0.12)
        # self.wait(5)
        # self.stop_ambient_camera_rotation()
        # self.wait(2)
    
    def create_tableau(self, matrix_data, basis_labels, z_val, solution, is_optimal=False):
        headers = [Text(t, font_size=16, color=BLUE_B, weight=BOLD) for t in ["RHS", "x₁", "x₂", "x₃", "x₄", "x₅", "x₆"]]
        data_cells = [[MathTex(str(c), font_size=16) for c in row] for row in matrix_data]
        table = MobjectTable([headers] + data_cells, include_outer_lines=True, h_buff=0.6, v_buff=0.3, line_config={"stroke_width": 2, "color": WHITE})
        title = Text("Simplex Tableau" if not is_optimal else "OPTIMAL TABLEAU", font_size=20, weight=BOLD, color=GOLD if is_optimal else BLUE_B)
        content = VGroup(title, table).arrange(DOWN, buff=0.3)
        bg = SurroundingRectangle(content, color=GOLD if is_optimal else BLUE, fill_opacity=0.15, stroke_width=3 if is_optimal else 2, buff=0.28)
        return VGroup(bg, content)