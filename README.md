*This project has been created as part of the 42 curriculum by lgirard.*

# Description
**Fly-In** is an efficient drone routing system that optimizes pathfinding through connected zones while minimizing simulation steps and handling movement constraints.

The project is divided into three main components:

- **Map Parsing**: Interprets map files according to specified format rules.
- **Map Solving**: Applies Dinitz's algorithm with time-expanded networks to compute optimal routing.
- **Visualization**: Renders the simulation with an interactive visualizer.

# Instructions

### Makefile Rules
- `install`: Install dependencies using uv.
- `run`: Run the project.
- `debug`: Run the project in debug mode with pdb.
- `lint`: Check code quality using Flake8 and MyPy.
- `lint-strict`: Check code quality using Flake8 and MyPy with strict flags.
- `clean`: Remove build artifacts.
- `fclean`: Remove all build artifacts and dependencies.


### Command-Line Flags
- `--map-path` / `-m`: Path to a specific map file.
- `--map-location` / `-ml`: Directory containing map files.
- `--output-file` / `-o`: Output file for results.


### Usage Example
```bash
make run ARGS="[--map-path MAP_PATH] [--map-location MAP_LOCATION] [--output-file OUTPUT_FILE]"
```

# Algorithm

This project uses **Dinitz's algorithm** with a time-expanded network to compute maximum flow routing.

### Solution Pipeline

1. **Time-Expanded Network**: Transform the original network into a layered time-expanded graph.
2. **Breadth-First Search (BFS)**: Compute level graphs for efficient flow computation.
3. **Depth-First Search (DFS)**: Calculate maximum flow through blocking flows.

### Why Dinitz's Algorithm?

Unlike single-path algorithms (Dijkstra, Floyd-Warshall), Dinitz's algorithm computes **multi-agent routing simultaneously** by calculating the network's max-flow; the maximum throughput from source to sink through a time-expanded network. This allows optimal routing for all drones at once rather than individually.

### Time-Expanded Network

A time-expanded network extends a standard spatial network by adding a temporal dimension. Each node in the original network is duplicated across multiple time layers (time steps), creating a layered graph structure.

**Why time-expanded networks matter:**

In a standard network, nodes represent physical locations and edges represent connections. A time-expanded network adds time as a dimension: node $(v, t)$ represents location $v$ at time step $t$. This transformation allows us to model:

- **Movement delays**: Each drone takes time to traverse from one zone to another
- **Capacity constraints**: Limited bandwidth per time step prevents congestion
- **Multi-agent scheduling**: Different drones can use the same connection at different times


By flattening the temporal dimension into the network structure, we can apply standard maximum flow algorithms (Dinitz's) to solve multi-agent routing as a single optimization problem rather than solving individual paths sequentially.

### Example

Here's our network before its time-expansion.

![](https://media.discordapp.net/attachments/860546628564942878/1506254208138219541/image.png?ex=6a0d980c&is=6a0c468c&hm=6a9d27a870749e7e79aee1e219a7e5401b82fa433b08d9808c7c31489d236925&=&format=webp&quality=lossless)

Here's the same network with a 3 step time-expension.

![](https://media.discordapp.net/attachments/860546628564942878/1506265597712007228/image.png?ex=6a0da2a7&is=6a0c5127&hm=7f974ff602a09a9159bf3afd24911401ba00bcfe451884432902eee9c5c1f336&=&format=webp&quality=lossless)

**How the time-expanded network grows:**

At each time step $t$, the network includes all nodes from previous time steps plus new layer representing the current time. 

- **Step 0 (t=0)**: The network contains only the starting node "st" at time $t_0$. 
- **Step 1 (t=1)**: New layer appears with three reachable states: 
  - Move to node "a" → node "a" at $t_1$
  - Move to node "b" → node "b" at $t_1$
  - Wait at "st" → node "st" at $t_1$

**Key insight**: The node "st" exists multiple times in the expanded network—once at each time step. Node $(st, t_0)$ and node $(st, t_1)$ represent the same physical location at different points in time. This separation allows the algorithm to track when drones occupy each zone.

### Breadth-First Search (BFS) - Level Graph Construction

In Dinitz's algorithm, BFS doesn't compute the maximum flow directly. Instead, it builds a **level graph**—a layered representation showing the shortest path distance from source to all other nodes.

**What the BFS does:**

1. Starting from the source node (start zone), BFS discovers nodes layer by layer
2. Each discovered node is assigned a **level** equal to its distance from the source
3. The BFS creates edges only between consecutive levels (from level $i$ to level $i+1$)
4. This level graph guides the subsequent DFS to find blocking flows efficiently

**Why this matters:**

This constrains the search space: BFS guarantees that only edges moving toward the sink are used, preventing inefficient loops. The level graph becomes the efficient search space for the DFS phase. Network constraints (blocked zones, capacity limits) are automatically handled through edge filtering.

### Depth-First Search (DFS) - Blocking Flow Computation

After BFS constructs the level graph, DFS finds **blocking flows**—multiple paths from source to sink simultaneously. A blocking flow is a maximal set of disjoint paths where at least one edge becomes saturated (reaches capacity).

**How DFS finds paths quickly:**

1. DFS traverses the level graph from source toward sink, searching for any path
2. When a path to sink is found, it pushes maximum flow through that path
3. It **removes saturated edges** (those that reached capacity limit) from the graph
4. DFS backtracks and immediately searches for alternative paths in the remaining graph
5. This continues until no more paths exist from source to sink

**Why it's efficient:**

- **Constrained search**: DFS only searches within the level graph (already pruned by BFS), not the entire network
- **Parallel path finding**: Multiple disjoint paths are found in a single DFS pass through blocking flows
- **Incremental removal**: Saturated edges are removed as they're used, gradually reducing the search space
- **Iteration**: BFS-DFS pairs repeat with updated capacities until maximum flow is reached

This combination ensures Dinitz's algorithm finds all routing paths rapidly: BFS identifies the most direct routes, while DFS finds multiple independent paths concurrently by exploiting capacity constraints.

### Main Loop

Dinitz's algorithm repeats until max-flow is lower than nb_drones:

1. **Expand Network**: Expand one step the network
1. **BFS phase**: Build level graph from current network
2. **DFS phase**: Find all blocking flows through the level graph
3. **Update**: Add blocking flow to max-flow, update residual capacities
4. **Repeat**: If max_flow is greater or equal nb_drones, stop. Otherwise, go to step 1.

Each iteration increases the max-flow. The algorithm terminates when the max-flow is greater than or equal to the number of drones, meaning we can send at most that many drones per step.

# Visualization

Real-time visualization of drone routing using Raylib.

**Features:**
- Zones displayed as colored circles, connections as gray lines
- White indicators show drones actively moving through connections
- Step-by-step animation showing drone positions and states
- Mouse hover reveals drone count and connection metadata
- Responsive scaling to fit any screen size

# Resources

- [Dinitz's Algorithm Tutorial](https://www.youtube.com/watch?v=M6cm8UeeziI)
- [Time-Expanded Networks](https://www.youtube.com/watch?v=yjPdeXb04VE)
- [Raylib Python Documentation](https://pypi.org/project/raylib/)