@REM manim-slides convert --open IntroSlide -cslide_number=true file.html @REM Good to know

manim-slides render ./viz/scenes/intro.py
@REM manim-slides render ./viz/scenes/odd_boards.py
@REM manim-slides render ./viz/scenes/color_matching.py
@REM manim-slides render ./viz/scenes/sabrinas_game.py
@REM manim-slides render ./viz/scenes/cnn.py
@REM manim-slides render ./viz/scenes/results.py

@REM manim-slides present ResultsSlide

@REM manim-slides present IntroSlide OddBoardsSlide ColorMatching SabrinasGame CNNSlide ResultsSlide