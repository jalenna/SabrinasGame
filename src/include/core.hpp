#pragma once
#include <vector>
#include <random>
#include <iostream>
#include <cassert>
#include <functional>
#include <utils.hpp>

class JAlgorithmBase
{
public:
    virtual ~JAlgorithmBase() = default;
    virtual void solve(std::function<float(float, float)> cost_func) = 0;
    virtual float get_cost() = 0;
};

struct JPair
{
    int x;
    int y;
};

class JGrid
{
private:
    int rows, cols;
    std::vector<float> cells;
    std::vector<std::vector<int>> neighbor_ids;
    std::function<float(float, float)> cmp;

private:
    void random_fill()
    {
        std::random_device rnd;
        std::mt19937 eng(rnd());
        std::uniform_real_distribution<float> dist(1, 100);
        std::generate(cells.begin(), cells.end(), [&]()
                      { return dist(eng); });
    }

    void reset_neighbor_ids()
    {
        neighbor_ids = std::vector<std::vector<int>>(rows * cols, std::vector<int>());

        for (int i = 0; i < (int)cells.size(); i++)
        {
            int row = i / rows;
            int col = i % cols;

            // Left
            if (col > 0)
                neighbor_ids[i].push_back(i - 1);
            // Right
            if (col + 1 < cols)
                neighbor_ids[i].push_back(i + 1);
            // Up
            if (row > 0)
                neighbor_ids[i].push_back(i - cols);
            // Down
            if (row + 1 < rows)
                neighbor_ids[i].push_back(i + cols);

            std::sort(neighbor_ids[i].begin(), neighbor_ids[i].end(), cmp);
        }
    }

public:
    JGrid(int rows, int cols, std::function<float(float, float)> cmp) : rows(rows), cols(cols), cells(rows * cols), cmp(cmp)
    {
    }

    void init()
    {
        random_fill();
        reset_neighbor_ids();
    }

    void set_grid(int n_rows, int n_cols, std::vector<float> n_cells)
    {
        assert(n_rows * n_cols == n_cells.size());

        if (n_rows != rows && n_cols != cols)
            reset_neighbor_ids();

        rows = n_rows;
        cols = n_cols;
        cells = std::move(n_cells);
    }

    const std::vector<float> &get_cells() const { return cells; }
    const std::vector<std::vector<int>> &get_all_neighbor_ids() const { return neighbor_ids; }
    const std::vector<int> get_neighbor_ids(int idx) const { return neighbor_ids[idx]; }
    const int get_rows() const { return rows; }
    const int get_cols() const { return cols; }
};