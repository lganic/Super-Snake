// hamilton_cycle_refactored.cpp
#include <vector>
#include <unordered_set>
#include <optional>
#include <algorithm>
#include <iostream>
#include <cassert>

// Define the graph as a vector of vectors
using Graph = std::vector<std::vector<int>>;

// Function to validate the graph
bool validate_graph(const Graph& graph) {
    int n = graph.size();
    for (const auto& neighbors : graph) {
        for (const auto& v : neighbors) {
            if (v < 0 || v >= n) {
                std::cerr << "Invalid vertex index detected: " << v << std::endl;
                return false;
            }
        }
    }
    return true;
}

// Function to check if adding vertex `v` to the current path is valid
bool is_valid(int v, int last, const std::vector<bool>& visited, const Graph& graph) {
    // Check if vertex `v` has already been visited
    if (visited[v]) return false;

    // Check if `v` is a neighbor of the last vertex in the path
    for (const auto& neighbor : graph[last]) {
        if (neighbor == v) return true;
    }
    return false;
}

// DFS function to find the Hamiltonian cycle
std::optional<std::vector<int>> dfs(const Graph& graph, std::vector<int>& path, std::vector<bool>& visited) {
    if (path.size() == graph.size()) {
        // Check if there's an edge back to the starting vertex to form a cycle
        int start = path.front();
        int last = path.back();
        for (const auto& neighbor : graph[last]) {
            if (neighbor == start) return path;
        }
        return std::nullopt;
    }

    int last = path.back();
    for (const auto& v : graph[last]) {
        if (is_valid(v, last, visited, graph)) {
            // Choose
            path.push_back(v);
            visited[v] = true;

            // Explore
            auto cycle = dfs(graph, path, visited);
            if (cycle.has_value()) {
                return cycle;
            }

            // Un-choose (backtrack)
            path.pop_back();
            visited[v] = false;
        }
    }
    return std::nullopt;
}

// Function to find a Hamiltonian cycle
std::optional<std::vector<int>> hamilton_cycle(const Graph& graph) {
    // Validate the graph first
    if (!validate_graph(graph)) {
        std::cerr << "Graph validation failed. Exiting." << std::endl;
        return std::nullopt;
    }

    if (graph.empty()) {
        std::cerr << "Empty graph provided. No Hamiltonian cycle exists." << std::endl;
        return std::nullopt;
    }

    // Initialize path and visited array
    std::vector<int> path = {0}; // Start from vertex 0
    std::vector<bool> visited(graph.size(), false);
    visited[0] = true;

    // Start DFS from the first vertex
    return dfs(graph, path, visited);
}