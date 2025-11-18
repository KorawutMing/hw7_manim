# SimplexPath3D - Manim Animation

This project contains a Manim animation that visualizes the Simplex algorithm path through a 3D polyhedron, showing the complete tableau at each iteration.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Instructions

### 1. Initialize Virtual Environment

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Manim and Required Libraries

Once your virtual environment is activated, install the required packages:

```bash
# Upgrade pip
pip install --upgrade pip

# Install Manim Community Edition
pip install manim

# Install NumPy (usually comes with Manim, but just in case)
pip install numpy
```

### 3. Verify Installation

Test that Manim is installed correctly:

```bash
manim --version
```

You should see output showing the Manim version (e.g., `Manim Community v0.18.0`).

## Running the Animation

### Render the Animation

To render the SimplexPath3D scene:

```bash
# High quality render (1080p, 60fps)
manim -pqh SimplexPath3D.py SimplexPath3D

# Medium quality render (720p, 30fps) - faster
manim -pqm SimplexPath3D.py SimplexPath3D

# Low quality render (480p, 15fps) - fastest for testing
manim -pql SimplexPath3D.py SimplexPath3D
```

### Command Flags Explanation:
- `-p`: Preview the animation after rendering
- `-q`: Quality settings
  - `l`: Low quality (480p15)
  - `m`: Medium quality (720p30)
  - `h`: High quality (1080p60)

### Output Location

The rendered video will be saved in:
```
media/videos/SimplexPath3D/[quality]/SimplexPath3D.mp4
```

## Project Structure

```
project/
│
├── SimplexPath3D.py       # Main Manim scene file
├── README.md              # This file
├── venv/                  # Virtual environment (created after setup)
└── media/                 # Output directory (created after first render)
    └── videos/
        └── SimplexPath3D/
```

## Troubleshooting

### Issue: LaTeX errors
**Solution:** Manim requires LaTeX for rendering mathematical text. Install LaTeX:
- **Windows**: Install MiKTeX from https://miktex.org/
- **macOS**: Install MacTeX with `brew install --cask mactex`
- **Linux**: Install with `sudo apt-get install texlive-full` (Ubuntu/Debian)

### Issue: ffmpeg not found
**Solution:** Install ffmpeg:
- **Windows**: Download from https://ffmpeg.org/ or use `winget install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### Issue: Slow rendering
**Solution:** 
- Use lower quality settings (`-pql`) for testing
- The first render is always slower as Manim caches textures
- Close other applications to free up system resources

## Animation Details

This animation demonstrates:
- 3D visualization of a linear programming feasible region
- Simplex algorithm path: A → D → B → C → E
- Complete Simplex tableaux at each iteration
- Optimal solution highlighting at vertex E(4, 4, 4)
- Objective function: Minimize Z = -10x₁ - 12x₂ - 12x₃

## Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

## Additional Resources

- [Manim Community Documentation](https://docs.manim.community/)
- [Manim Discord Community](https://discord.gg/manim)
- [Example Gallery](https://docs.manim.community/en/stable/examples.html)

## License

This project is provided as-is for educational purposes.