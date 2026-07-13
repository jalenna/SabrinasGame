from manim import *
from random import seed as rand_seed
from manim_slides.slide import ThreeDSlide

config["max_files_cached"] = -1


class ResultsSlide(ThreeDSlide):
    skip_reversing = True

    _required_tiles: int = 0
    _curr_num_tiles: int = 0

    def construct(self) -> None:
        rand_seed(42)

        avg_dfs, avg_guided = 0, 0
        avg_dfs_forw, avg_guided_forw = 0, 0
        avg_dfs_backw, avg_guided_backw = 0, 0
        with open("dfs_vs_guided.csv") as f:
            f.readline()
            _, avg_dfs, avg_guided = f.readline().split(",")
            _, avg_dfs_forw, avg_guided_forw = f.readline().split(",")
            _, avg_dfs_backw, avg_guided_backw = f.readline().split(",")

        table: Table = Table([
            [avg_dfs, avg_guided],
            [avg_dfs_forw, avg_guided_forw],
            [avg_dfs_backw, avg_guided_backw]
        ],
            col_labels=[
            Text("DFS"),
            Text("CNN Guided DFS"),
        ],
            row_labels=[
            Text("Cost"),
            Text("Forward"),
            Text("Backward"),
        ]
        )

        slide_number: Text = Text("23/24").move_to(DOWN * 7. + RIGHT * 13.)
        self.play(Write(slide_number), Create(table))

        _, _, _, _, zoom = self.camera.get_value_trackers()
        self.play(
            AnimationGroup((zoom.animate.set_value(.5),),
                           run_time=3, rate_func=rate_functions.ease_in_out_circ
                           )
        )

        self.next_section()

        self.fade_all_out()

        questions: Text = Text("Thank You! Any questions?")

        t_slide_number: Text = Text("24/24").move_to(DOWN * 7. + RIGHT * 13.)

        self.play(Write(questions), ReplacementTransform(
            slide_number, t_slide_number))

        slide_number = t_slide_number

    def fade_all_out(self, run_time=.2) -> None:
        self.play(
            *[FadeOut(mob, run_time=run_time)for mob in self.mobjects]
        )
