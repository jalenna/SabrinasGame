@REM manim-slides convert --open IntroSlide -cslide_number=true file.html @REM Good to know

@REM manim-slides render ./src/viz/scenes/intro.py
@REM manim-slides render ./src/viz/scenes/odd_boards.py
@REM manim-slides render ./src/viz/scenes/color_matching.py
@REM manim-slides render ./src/viz/scenes/sabrinas_game.py
@REM manim-slides render ./src/viz/scenes/cnn.py
@REM manim-slides render ./src/viz/scenes/mcmf.py
@REM manim-slides render ./src/viz/scenes/results.py
@REM manim-slides render ./src/viz/scenes/conclusion.py

@REM manim-slides convert --open IntroSlide OddBoardsSlide ColorMatching SabrinasGame CNNSlide ResultsSlide MCMFSlide ConclusionSlide file.html

@REM manim-slides present ResultsSlide

@REM manim-slides present IntroSlide OddBoardsSlide ColorMatching SabrinasGame CNNSlide ResultsSlide MCMFSlide ConclusionSlide

manim-slides render ./src/main.py && manim-slides present Presentation
@REM manim-slides convert --open Presentation present.html
@REM manim-slides render -ql ./src/main.py && manim-slides present Presentation