@REM manim-slides convert --open IntroSlide -cslide_number=true file.html @REM Good to know

@REM manim-slides render ./viz/scenes/intro.py
@REM manim-slides render ./viz/scenes/odd_boards.py
@REM manim-slides render ./viz/scenes/color_matching.py
manim-slides render ./viz/scenes/sabrinas_game.py
manim-slides present SabrinasGame

@REM manim-slides present IntroSlide OddBoardsSlide ColorMatching SabrinasGame @REM Finale