#include <string>
#include <cstdlib>

int main(int argc, char *argv[])
{
    std::string cur = argv[0];

    while (cur[cur.size() - 1] != '/')
    {
        cur.pop_back();
        if (cur.size() == 0)
        {
            cur = "./";
            break;
        }
    }
    cur += "bin/";

    std::string cmd = "cd \"" + cur + "\" && ./main";
    system("clear");
    system(cmd.c_str());

    return 0;
}
