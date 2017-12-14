#include <vector>
#include "api_player.h"
#include "communicate.h"

using std::vector;

vector<Command> command_queue;
bool askUpdateAge = false;

void updateAge()
{
    askUpdateAge = true;
}

void construct(BuildingType building_type, Position pos, Position solider_pos)
{
    command_queue.push_back(Command(Construct, building_type, pos, solider_pos));
}

void upgrade(int unit_id)
{
    command_queue.push_back((Command(Upgrade, unit_id)));
}

void sell(int unit_id)
{
    command_queue.push_back((Command(Sell, unit_id)));
}

void toggleMaintain(int unit_id)
{
    command_queue.push_back((Command(Maintain, unit_id)));
}