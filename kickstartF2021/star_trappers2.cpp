#include <iostream>
#include <vector>
#include <string>

using namespace std;

string solution(vector<vector<int> > points) {
    printf("\n");
    for (vector<int> p : points) {
        printf("%d %d\n",p[0], p[1]);
    }
    return "some result";

}
int main() {
    int T, N, X, Y;
    vector<vector<int> > points;
    string result;

    cin >> T;
    for (int i = 1; i <= T; i++) {
        points.clear();

        cin >> N;
        for (int j = 0; j <= N; j++) {
            cin >> X >> Y;
            points.push_back({X, Y});
        }
        result = solution(points);

        cout << "Case #" << i << ": " << result << endl;
    }
    return 0;
}
