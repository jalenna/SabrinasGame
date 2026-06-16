from manim import Code, FadeIn
from manim_slides.slide import Slide
from manim import config as global_config

global_config.fullscreen = True


class ConvertExample(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.1

        code = Code(
            code_string="""#include <iostream>
#include "./include/core.hpp"
#include "./include/algorithms/algorithms.hpp"
#include <math.h>

int main()
{
    JGrid grid(15, 15);
    grid.init();

    auto sort_func = [](float a, float b)
    {
        if (std::abs(a) != std::abs(b))
            return std::abs(a) > std::abs(b);
        return a > b;
    };

    auto cost_func = [](float a, float b)
    { return (a > b) ? a - b : b - a; };

    JDFSAlgorithm dfs(grid);
    JAlgorithmBase *a = &dfs;

    a->solve(cost_func, sort_func);

    std::cout << "AVG cost: " << a->get_cost() << std::endl;
    return 0;
}
""",
            language="C++",
            formatter_style="inkpot"
        )

        code.scale(0.5)

        self.play(FadeIn(code))
