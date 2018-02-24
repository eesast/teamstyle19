#include"api_player.h"
#include<vector>
#include"communication.h"
using namespace std;

bool _updateAge;
vector<command1> c1;
vector<command2>c2;

void updateAge()
{
	_updateAge = true;
}
void construct(BuildingType building_type, Position pos, Position solider_pos) //The solier position is not set now
{
	//solider position 是干什么的？？？
	c2.push_back(command2(int(building_type), 1, pos.x, pos.y,solider_pos.x,solider_pos.y));
}
void upgrade(int unit_id)
{
	c1.push_back(command1(unit_id, 2));
}
void sell(int unit_id)
{
	c1.push_back(command1(unit_id, 3));
}
void toggleMaintain(int unit_id)
{
	c1.push_back(command1(unit_id, 4));
}
