# CoordCA
A bad Python Cellular Automata simulator with arbitrary neighborhood and infinite universe.

## Contents
* [Usage](#usage)
* [What is This?](#what-is-this)
* [The GUI](#the-gui)
	- [The Menu Bar](#the-menu-bar)
	- [The Status Bar](#the-status-bar)
	- [The Tools Bar](#the-tools-bar)
* [Formats](#formats)
	- [Rule Format](#rule-format)
	- [RLE](#rle)
	- [CCA](#cca)
* [Known Bugs](#known-bugs)
* [Planned Additions](#planned-additions)

## Usage
There are two ways to use CoordCA, the first is to simply open the executable file.
The second way is to use Python to run it. This is obviously useful when making modifications to the program. The source code can be found in the "source" folder.

## What is This?
CoordCA is a program for simulating 2-state Totalistic Cellular Automata (CA) with arbitrary neighborhood.
A Cellular Automata or CA is a "0-player game" where each cell has neighbors and changes state depending
on it's neighbors.

The neighbors a cell has depends on its neighborhood, which is the set of cells every cell has to check.
This set of cells is defined relative to the each cell. For example, this is a Moore neighborhood:
```
111
1c1
111
```
In each step (generation) in a 2-state Totalistic CA, every cell will count how many neighbors it has. 
If the center cell is in a "live" state and does not have the correct amount of neighbors, 
it will become "dead". If a cell in a "dead" state has the correct amount of neighbors, it will become alive.

## The GUI
CoordCA has a non-professionally designed GUI which consists of a menu bar at the very top, a status bar below,
and a row of buttons below that called the "tools bar". It also has a grid for viewing.

### The Menu Bar
CoordCA has a bar on top with a bunch of dropdown menus to do what you need. Here's what each button does.

#### Pattern Menu
**New Universe:** Create a new, empty universe with the current rule.
**Read Pattern:** Open a pattern file in RLE or CCA format.
**Save Pattern:** Save the current pattern.
**Copy Pattern (RLE):** Copy the entire current pattern in RLE format.
**Copy Pattern (Coords):** Copy the entire current pattern in CCA format.

**Draw:** Set cursor to drawing mode.

#### Viewing Menu
**Zoom In:** Zoom in / Make the cells bigger.
**Zoom Out:** Zoom Out / Make the cells smaller.
**Go to:** Move to where the top left cell's coordinates are the specified values.

**Colors:** Change the colors of the live and dead cells.
**Toggle Lines:** Toggle the grid lines.

#### Simulation Menu
**Next Generation:** Run the pattern for one generation.
**Start:** Start running the pattern.
**Stop:** Stop running the pattern.
**Reset:** Reset the pattern to whatever it was at generation 0.

**Set Rule:** Change the current rule.
**Get Neighborhood List:** Get the list of neighborhood in list-of-tuples form.
**Generate APGtable:** Automatically generate a table for apgluxe.

#### Selection
**Remove Selection:** Remove the current selection.
**Clear Inside Selection:** Clear the selection.
**Random Fill:** Fill the selection with random cells.

#### Help Menu
**About:** Tells information about the program.
**Credits:** Some credits for the program.
**Secret Debug Button:** Well, it's secret.

### The Status Bar
The yellow ribbon on the top is the status bar. 
It displays the current generation, population, rule, and coordinates of the top left cell (View X and View Y)

### The Tools Bar
The tools bar is a row of buttons that can be found below the status bar.
The buttons are:
* **Step:** Run the pattern for one generation.
* **Reset:** Reset the pattern to whatever it was at generation 0.
* **Run:** Toggle automatic generation of the pattern.
* **Draw:** Set cursor to draw mode. Click a cell to toggle its state.
* **Move:** Set cursor to move mode. Drag the cursor to pan.
* **Select:** Set cursor to select mode. Drag the cursor to create a selection. Click to remove the selection.
* **Zoom In:** Zoom in.
* **Zoom out:** Zoom out.

## Formats
CoordCA has lots (Like 3) of different formats for different stuff, and those formats will be explained below.
### Rule Format
The rule format used by CoordCA is comprised of 3 parts, separated by underscores (_).
The first part of the rule is the neighborhood used. It is a hexadecimal string number starting with 1.
A neighborhood is defined like this:

\1. Draw the neighborhood as a square with 1s and 0s.
   1 indicates the cell is part of the neighborhood.
```
   10001
   00100
   01c10
   00100
   10001
```
   "c" is the center cell that will be checked when running a pattern.

\2. Remove line breaks, erase the center, and add a 1 in front.
   ```1100010010001100010010001```
   
\3. Convert to Hexadecimal.
   ```1891891```
   
That is our neighborhood. Next, we specify the range of the neighborhood.
This is the distance from the center to the edge of our square in cells.
In this case, our range is 2. Add that to the rulestring separated by a hyphen (-).
```1891891-2```

The next part is the birth.
A dead cell with the right ammount of neighbors will be born the next generation.
Each birth value will be separated by a hyphen.
```1891891-2_3```

The next part is survival.
This is similar to birth.
A live cell with the wrong amount of neighbors will die the next generation.
Again, each value will be separated by a hyphen.
```1891891-2_3_2-3```

That is our ruleString!

### RLE
Please see [this page](http://www.conwaylife.com/wiki/Rle)

### CCA
A CCA file encodes the coordinates of the live cells as well as the rule.
A CCA has two parts, separated by a colon (:).
The first part is the rule (Described above).
The second part is a list of tuples which are the coordinates of the live cells.
Example of a pattern in CCA format:
```1891891-2_3_2-3:[(0, 1), (1, 1), (2, 1), (2, 0), (4, 0), (4, 1), (4, 2), (3, 2), (5, 2), (2, 3), (2, 4)]```

## Known Bugs
* Program sometimes crashes when selecting.
* Cell at 0,0 toggled when mouse starts on grid on opening the program.

## Planned Additions
* Ability to use multiple algorithms to simulate different rules.
* Ability to implement a custom algorithm easily.
* Enter as a substitute for "Ok".
* Icons instead of text.
