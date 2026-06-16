#include <iostream>
#include "./include/core.hpp"
#include "./include/algorithms/algorithms.hpp"
#include <math.h>

int main()
{
    auto cost_func = [](float a, float b)
    { return (a > b) ? a - b : b - a; };

    JGrid grid(5, 5, cost_func);
    grid.init();

#ifdef LOG
    write_step("Test");
    close_steps_file();
#endif

    JDFSAlgorithm dfs(grid);
    JAlgorithmBase *a = &dfs;

    a->solve(cost_func);

    std::cout << "AVG cost: " << a->get_cost() << std::endl;
    return 0;
}