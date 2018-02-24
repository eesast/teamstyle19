#include"communication.h"
#include<thread>
#include<vector>
#include<iostream>
#include<ctime>
using namespace std;

extern	bool _updateAge;
extern vector<command1> c1;
extern vector<command2> c2;
void f_player();

State* state=NULL;
MyClient cilent;
bool** map;
bool flag;

void Listen()
{
	State* t;
	while (true)
	{
		State* s = cilent.recv_state();
	//	cout << "!!!!!!!!---------------!!!!!" << s->turn << endl;
		//delete _listen;
		//_listen = s;
		t=state;
		state = s;
		delete t;
	}
}

int main()
{
	for (int i = 0; i < 50; i++)
		c1.push_back(command1(i, 3));
	for (int i = 0; i < 50; i++)
		c2.push_back(command2(6, i + 10, 4, 4, 5, 5)); //测试用的
	cilent.start_connection();
	map = cilent.map;
	flag = cilent.flag;
	int turn = 0;
	thread th_communication(Listen);
	//State* state;
	while (state == NULL)
	{

	}
	State* laststate = NULL;
	while (state->turn < 1000)
	{
		if (state == NULL)
			continue;
		if (state == laststate)
			continue;
		laststate = state;
		if (state->turn == 30)
		{
			int ee;
			cin >> ee;
		}
		cout << "********************"<<state->turn <<"****************************"<< endl;
		if (state->winner != 3)//出现了胜利者
			break;
		f_player();
		cilent.send_command(_updateAge,c1,c2);
		_updateAge = false;
		//c1.clear();//注 如果f_player()是空的 最好去掉clear 否则会发空指令 没意义
		c2.clear();
		Sleep(100);
		cout << "********************************************************" << endl;
	}
	if (state->winner == 1)
		cout << "Winner is 1" << endl;
	else if (state->winner == 0)
		cout << "Winner is 0" << endl;
	else if (state->winner == 3)
		cout << "draw" << endl;
}