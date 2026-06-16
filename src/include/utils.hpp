#pragma once

#ifdef LOG
#include <iostream>
#include <fstream>
#include <string>

const char *steps_file = "algorithm_steps.txt";
std::ofstream steps_file_stream(steps_file);

void write_step(const char *content)
{
    steps_file_stream << content;
}

void close_steps_file()
{
    steps_file_stream.close();
}

#endif