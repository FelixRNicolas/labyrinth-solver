#include <bits/stdc++.h>
using namespace std;

const vector<int> GOAL = {
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 0
};

struct Node {
    vector<int> state;
    vector<char> path;
    int cost;
    int heuristic;

    int f() const { return cost + heuristic; }
    bool operator>(const Node &other) const {
        return f() > other.f();
    }
};

map<char,int> MOVES = {
    {'U', -4}, {'D', 4}, {'L', -1}, {'R', 1}
};

bool is_valid_move(int pos, char move) {
    if (move == 'L' && pos % 4 == 0) return false;
    if (move == 'R' && pos % 4 == 3) return false;
    if (move == 'U' && pos < 4) return false;
    if (move == 'D' && pos > 11) return false;
    return true;
}

vector<pair<vector<int>, char>> get_neighbors(const vector<int>& state) {
    vector<pair<vector<int>, char>> neighbors;
    int pos = int(find(state.begin(), state.end(), 0) - state.begin());
    for (auto &p : MOVES) {
        char move = p.first;
        int offset = p.second;
        if (is_valid_move(pos, move)) {
            vector<int> new_state = state;
            int new_pos = pos + offset;
            swap(new_state[pos], new_state[new_pos]);
            neighbors.push_back({new_state, move});
        }
    }
    return neighbors;
}

void print_board(const vector<int>& state) {
    for (int i = 0; i < 16; ++i) {
        if (state[i] == 0) cout << "   ";
        else cout << setw(2) << state[i] << ' ';
        if (i % 4 == 3) cout << '\n';
    }
    cout << '\n';
}

void show_solution(const vector<int>& start, const vector<char>& path) {
    vector<int> current = start;
    cout << "Estado inicial:\n";
    print_board(current);
    for (char move : path) {
        int pos = int(find(current.begin(), current.end(), 0) - current.begin());
        int new_pos = pos + MOVES[move];
        swap(current[pos], current[new_pos]);
        cout << "Movimiento: " << move << '\n';
        print_board(current);
    }
}

// BFS (no heurística) - puede explotar en memoria para estados grandes.
vector<char> bfs(const vector<int>& start) {
    queue<pair<vector<int>, vector<char>>> q;
    set<vector<int>> visited;
    q.push({start, {}});
    visited.insert(start);

    while (!q.empty()) {
        auto [state, path] = q.front(); q.pop();
        if (state == GOAL) return path;
        for (auto &nb : get_neighbors(state)) {
            auto &neighbor = nb.first;
            char move = nb.second;
            if (!visited.count(neighbor)) {
                visited.insert(neighbor);
                auto new_path = path;
                new_path.push_back(move);
                q.push({neighbor, new_path});
            }
        }
    }
    return {};
}

int manhattan_distance(const vector<int>& state) {
    int distance = 0;
    for (int i = 0; i < 16; ++i) {
        int tile = state[i];
        if (tile == 0) continue;
        int goal_x = (tile - 1) % 4;
        int goal_y = (tile - 1) / 4;
        int x = i % 4, y = i / 4;
        distance += abs(x - goal_x) + abs(y - goal_y);
    }
    return distance;
}

vector<char> astar(const vector<int>& start) {
    priority_queue<Node, vector<Node>, greater<Node>> pq;
    set<vector<int>> visited;

    Node startNode{start, {}, 0, manhattan_distance(start)};
    pq.push(startNode);

    while (!pq.empty()) {
        Node node = pq.top(); pq.pop();
        if (node.state == GOAL) return node.path;
        if (visited.count(node.state)) continue;
        visited.insert(node.state);

        for (auto &nb : get_neighbors(node.state)) {
            const vector<int>& neighbor = nb.first;
            char move = nb.second;
            if (!visited.count(neighbor)) {
                vector<char> new_path = node.path;
                new_path.push_back(move);
                int new_cost = node.cost + 1;
                int h = manhattan_distance(neighbor);
                pq.push(Node{neighbor, new_path, new_cost, h});
            }
        }
    }
    return {};
}

// Comprueba si el puzzle es resoluble (regla estándar para 4x4)
bool is_solvable(const vector<int>& state) {
    int inversions = 0;
    vector<int> flat;
    for (int tile : state) if (tile != 0) flat.push_back(tile);

    for (int i = 0; i < (int)flat.size(); ++i)
        for (int j = i + 1; j < (int)flat.size(); ++j)
            if (flat[i] > flat[j]) ++inversions;

    int blank_pos = int(find(state.begin(), state.end(), 0) - state.begin());
    int row_from_bottom = 4 - (blank_pos / 4); // 1..4 counting from bottom

    if ((row_from_bottom % 2 == 0) == (inversions % 2 == 0)) return false;
    return true;
}

int main() {
    vector<int> start = {
        1, 2, 3, 4,
        5, 9, 7, 0,
        6, 10, 11, 0,
        15, 14, 13, 12
    };

    if (!is_solvable(start)) {
        cout << "Este tablero NO es resoluble.\n";
        return 0;
    }

    cout << "Resolviendo con A*...\n";
    auto path_astar = astar(start);

    if (path_astar.empty()) {
        cout << "No se encontró solución con A* (posible límite de memoria/tiempo).\n";
        return 0;
    }

    cout << "Secuencia de movimientos: ";
    for (char m : path_astar) cout << m << ' ';
    cout << '\n' << '\n';

    show_solution(start, path_astar);
    return 0;
}
