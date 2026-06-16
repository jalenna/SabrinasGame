#pragma once
#include "../core.hpp"
#include <ranges>

class JDFSAlgorithm : public JAlgorithmBase
{
private:
    JGrid &grid;

    // Cache
    int rows = grid.get_rows();
    int cols = grid.get_cols();
    int required_num_tiles = (rows * cols) / 2;
    const std::vector<float> &cells = grid.get_cells();

    std::vector<int> pairs;
    int current_num_tiles = 0;
    float cost = -1.f;

    void _solve(int curr_node)
    {
        auto cmp_f = [&](const int a)
        {
            return pairs[a] == -1 && a != curr_node;
        };

        const auto &neighbors = grid.get_neighbor_ids(curr_node);

        auto filtered_neighbors = std::views::filter(neighbors, cmp_f);

        // Exhausted || Done
        if (filtered_neighbors.empty() || current_num_tiles == required_num_tiles)
            return;

        for (const int &next_best : filtered_neighbors)
        {
            // Pair current
            pairs[curr_node] = next_best;
            pairs[next_best] = curr_node;

            current_num_tiles++;

            const auto &next_best_neighbors = grid.get_neighbor_ids(next_best);

            auto filtered_next_best_neighbors = std::views::filter(next_best_neighbors, cmp_f);

            //   Look at next possible pair
            for (const int &filtered_next_best : filtered_next_best_neighbors)
                _solve(filtered_next_best);

            // Solution incorrect
            if (current_num_tiles != required_num_tiles)
            {
                pairs[curr_node] = -1;
                pairs[next_best] = -1;
                current_num_tiles--;
            }
            else
                return;
        }
    }

public:
    JDFSAlgorithm(JGrid &grid) : grid(grid)
    {
        pairs = std::vector<int>(rows * cols, -1);
    }

    void solve(std::function<float(float, float)> cost_func) override
    {
        _solve(0);

        if (required_num_tiles == current_num_tiles)
        {
            cost = 0.f;
            for (int i = 0; i < current_num_tiles; i++)
            {
                if (pairs[i] > i)
                    cost += cost_func(cells[pairs[i]], cells[i]);
            }
            cost /= current_num_tiles;
        }
    }

    float get_cost() override
    {
        return cost;
    }
};