
# ✨ Mach-Math — Linear Algebra Course

> Visual, animated explanations of the mathematics behind machine learning and AI — built with [Manim](https://www.manim.community/).

This repository contains the source code (Manim scenes, scripts, and shared assets) for the **Linear Algebra** course on the [Mach-Math](https://www.youtube.com/@Mach-Math) YouTube channel.

---

## 📺 About the Channel

**MACH-MATH** explains machine learning and AI algorithms visually, using simulation and animation tools (Manim). We start from linear algebra fundamentals and build up, step by step, until we reach a deep, geometric understanding of the algorithms powering today's AI.

If you want to understand the math *behind* AI — not just use it as a black box — this channel is for you.

🔗 [Subscribe on YouTube](https://www.youtube.com/@Mach-Math)

---

## 📚 Course Roadmap

The course is organized into three progressive playlists:

- [ ] **01 — Foundational Linear Algebra**
  Vectors, matrices, linear transformations, systems of equations.
- [ ] **02 — Intermediate Linear Algebra**
  Determinants, eigenvalues & eigenvectors, vector spaces, orthogonality.
- [ ] **03 — Advanced Linear Algebra**
  Decompositions (SVD, eigendecomposition), applications in ML & deep learning.

---

## 📂 Repo Structure

```
linear-algebra-course/
├── common/              # Shared intro/outro scenes, color palette, custom mobjects
├── 01-foundational/      # Scenes for the Foundational playlist
├── 02-intermediate/      # Scenes for the Intermediate playlist
├── 03-advanced/          # Scenes for the Advanced playlist
├── assets/               # Fonts, images, static resources
├── pyproject.toml
└── uv.lock
```

Each video's scene lives in its own file, numbered to match its position in the playlist (e.g. `01-foundational/02_matrix_multiplication.py`).

---

## 🛠 Tech Stack

- **[Manim Community Edition](https://www.manim.community/)** — mathematical animation engine (Python)
- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** — dependency & environment management

---

## 🚀 Getting Started

### Using `uv` (recommended — fast ⚡)

```bash
# Clone the repo
git clone https://github.com/ahmed-abualsaud/linear-algebra-course.git
cd linear-algebra-course

# Sync dependencies and create the environment automatically
uv sync

# Render a scene (low quality preview)
uv run manim -pql 01-foundational/01_vectors.py VectorsScene
```

### Using `pip`

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -e .

manim -pql 01-foundational/01_vectors.py VectorsScene
```

---

## 🤝 Contributing

Found a bug in an animation, or have a suggestion for a clearer explanation? Feel free to open an issue or a pull request.

---

## 📝 License

Course code is shared for educational purposes. See [LICENSE](LICENSE) for details.

---

<div align="center">
