#include<iostream>
#include<fstream>
#include<string>

using namespace std;

int main()
{
	string queryId;
	cout << "Query: ";
	cin >> queryId;
	string videoId;
	int frameId;
	cout << "videoId: ";
	cin >> videoId;
	cout << "frameId: ";
	cin >> frameId;

	ofstream fo("submissions/query-" + queryId + ".csv");
	fo << videoId << "," << frameId << "\n";
	for (int i = 1; i <= 49; ++i)
		fo << videoId << "," << frameId + i * 10 << "\n";
	for (int i = 1; i <= 49; ++i)
		fo << videoId << "," << max(0, frameId - i * 10) << "\n";
}
	


