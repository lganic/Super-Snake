// bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "hamilton_cycle.cpp" // Include your C++ implementation

namespace py = pybind11;

PYBIND11_MODULE(hamilton_cycle_module, m) {
    m.doc() = "Module to find Hamiltonian cycles in a graph";

    m.def("hamilton_cycle", [](const std::vector<std::vector<int>>& graph) -> py::object {
        auto cycle = hamilton_cycle(graph);
        if (cycle.has_value()) {
            return py::cast(cycle.value());
        } else {
            return py::cast(std::vector<int>());
        }
    }, "Find a Hamiltonian cycle in the given graph");
}
