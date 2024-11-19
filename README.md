# Pygame Map Editor

A Pygame-based tool for creating and editing maps. This project enables users to design maps by interacting with a grid interface and save/load their progress in `.map` files. It provides useful features like undo functionality, copying/pasting tiles, and custom color palettes.

---
![image](https://github.com/user-attachments/assets/f1e844a6-1765-4310-ae95-2ec27872053f)

## Features

- **Grid-based Editing**: Draw and edit maps using a simple grid layout.
- **Save & Load**: Save maps as `.map` files and load them for further editing.
- **Undo Support**: Revert recent changes with the undo functionality.
- **Custom Tile Colors**: Easily switch between predefined tile colors.
- **Keyboard & Mouse Interactions**: Intuitive control scheme for fast map editing.
- **File Management**: Create new maps and switch between files directly in the application.

---

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.7 or higher
- Pygame library

---

## Getting Started

1. Clone the repository:
   
   ```bash
   git clone https://github.com/yourusername/pygame-map-editor.git
   cd pygame-map-editor
   ```
2. Install required  dependencies:
   
   ```bash
   pip install pygame
   ```
3. Run the application:
   
   ```bash
   python map_editor.py
   ```
## Usage

### Controls:
- **Mouse**: Left-click to place a tile, right-click to erase.
- **Keyboard**:
  - `Ctrl + S`: Save the current map.
  - `Ctrl + O`: Open an existing `.map` file.
  - `Ctrl + N`: Create a new map.
  - `Ctrl + Z`: Undo the last action.
  - Arrow keys: Navigate around the map grid.

### File Management:
- Saved maps are stored in the `.map` format and can be opened for future editing.
- Use the file management interface within the editor to manage maps.

### Color Palette:
- Predefined tile colors can be selected via an intuitive menu system.
- Each tile type corresponds to a unique ID and color.
