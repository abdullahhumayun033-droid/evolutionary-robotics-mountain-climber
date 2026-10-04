# Evolutionary Robotics: Mountain-Climbing Creatures

A **CM3020 Artificial Intelligence** project exploring evolutionary robotics with **Python**, **PyBullet** and genetic algorithms.

The project encodes robot morphology and motor-controller parameters in a genome, converts those genomes into articulated URDF creatures, evaluates them in physics simulation and applies evolutionary operators to search for increasingly effective locomotion and mountain-climbing behaviour.

## Project Highlights

- Genetic encoding of robot morphology and controller parameters
- Procedural creature / URDF generation
- PyBullet physics simulation
- Population-based evaluation
- Fitness-driven parent selection
- Crossover and mutation
- Grow / shrink mutation
- Elitism
- Procedural motor control
- Mountain terrain experiments
- Recorded evolutionary-learning results

## AI Pipeline

1. **Encode** — each genome stores parameters describing links, joints and motor behaviour.
2. **Generate** — genomes are converted into articulated robot structures.
3. **Simulate** — creatures are evaluated in PyBullet.
4. **Measure fitness** — simulated behaviour is scored.
5. **Evolve** — selection, crossover and mutation generate the next population.
6. **Repeat** — successive generations search for improved behaviour.

## Repository Structure

```text
.
├── index.html
├── requirements.txt
├── assets/
│   ├── demo-highlight.mp4
│   └── demo-poster.jpg
├── part-a-core/
├── evolutionary-ga-framework/
└── docs/
```

## Live Showcase

A visual project page with an embedded demonstration video is available through GitHub Pages once Pages is enabled for this repository.

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

The recovered project uses PyBullet-based simulation. Individual scripts and tests are organised inside the source folders.

## Recovery Note

The recovered ZIP contains the core creature-genome, URDF-generation, motor, population and simulation code together with a genetic-algorithm framework and mountain assets.

The submitted presentation video also shows later Part B mountain-climbing experiments and evolutionary learning curves. The exact standalone final Part B experiment script visible in that recording was not present in the recovered archive, so this repository does not claim full reproducibility of every final chart shown in the presentation.

## Technologies

- Python
- PyBullet
- NumPy
- Genetic Algorithms
- Evolutionary Robotics
- URDF
- Physics Simulation

## Coursework Context

This repository is a cleaned portfolio version of a **University of London BSc Computer Science — CM3020 Artificial Intelligence** project.

## Author

**Abdullah Humayun**  
BSc Computer Science — University of London / Goldsmiths
