// hamilton_cycle_multithreaded.cpp
#include <iostream>
#include <vector>
#include <unordered_set>
#include <optional>
#include <thread>
#include <mutex>
#include <atomic>
#include <algorithm>

// Define the graph as a vector of vectors
using Graph = std::vector<std::vector<int>>;

// Function to check if adding vertex `v` to the current path is valid
bool is_valid(int v, const std::vector<int>& path, const Graph& graph) {
    if (std::find(path.begin(), path.end(), v) == path.end()) {
        if (path.empty()) {
            return true;
        } else {
            int last = path.back();
            return std::find(graph[last].begin(), graph[last].end(), v) != graph[last].end();
        }
    }
    return false;
}

// DFS function to find the Hamiltonian cycle
void dfs(const Graph& graph, std::vector<int> path,
         std::optional<std::vector<int>>& local_cycle,
         std::mutex& cycle_mutex, std::atomic<bool>& found) {
    if (found.load()) return; // Early exit if cycle is found

    if (path.size() == graph.size()) {
        // Check if there's an edge back to the starting vertex
        int start = path.front();
        int last = path.back();
        if (std::find(graph[last].begin(), graph[last].end(), start) != graph[last].end()) {
            std::lock_guard<std::mutex> lock(cycle_mutex);
            if (!found.load()) { // Double-check locking
                local_cycle = path;
                found.store(true);
            }
        }
        return;
    }

    int last = path.back();
    for (const auto& v : graph[last]) {
        if (is_valid(v, path, graph)) {
            std::vector<int> new_path = path;
            new_path.push_back(v);
            dfs(graph, new_path, local_cycle, cycle_mutex, found);
            if (found.load()) return; // Early exit
        }
    }
}

// Function to find a Hamiltonian cycle using multithreading
std::optional<std::vector<int>> hamilton_cycle(const Graph& graph) {
    if (graph.empty()) return std::nullopt;

    // Local shared variables
    std::optional<std::vector<int>> local_cycle;
    std::mutex cycle_mutex;
    std::atomic<bool> found(false);

    std::vector<std::thread> threads;
    // You can limit the number of threads based on hardware concurrency
    unsigned int max_threads = std::thread::hardware_concurrency();
    if (max_threads == 0) max_threads = 4; // Fallback if hardware_concurrency is not defined

    // Function to process a subset of starting vertices
    auto process_vertices = [&](int start_vertex) {
        if (found.load()) return;
        std::vector<int> path = {start_vertex};
        dfs(graph, path, local_cycle, cycle_mutex, found);
    };

    // Launch threads, distributing starting vertices among them
    for (int start_vertex = 0; start_vertex < graph.size(); ++start_vertex) {
        if (found.load()) break;
        if (threads.size() >= max_threads) {
            // Wait for the first thread to finish
            threads.front().join();
            threads.erase(threads.begin());
        }
        threads.emplace_back(process_vertices, start_vertex);
    }

    // Join all remaining threads
    for (auto& t : threads) {
        if (t.joinable()) t.join();
    }

    return local_cycle;
}

int main() {
    // Example usage:
    // Define a graph with 4 vertices forming a cycle: 0-1-2-3-0
    Graph graph = {
        {1, 3},    // Neighbors of vertex 0
        {0, 2},    // Neighbors of vertex 1
        {1, 3},    // Neighbors of vertex 2
        {0, 2}     // Neighbors of vertex 3
    };

    auto cycle = hamilton_cycle(graph);
    if (cycle) {
        std::cout << "Hamiltonian cycle found: ";
        for (const auto& v : *cycle) {
            std::cout << v << " ";
        }
        // To complete the cycle, you can print the start vertex again
        std::cout << cycle->front() << std::endl;
    } else {
        std::cout << "No Hamiltonian cycle exists." << std::endl;
    }

    return 0;
}
