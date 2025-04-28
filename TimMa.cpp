#include <bits/stdc++.h>
using namespace std;

string maHoa(string s, int k)
{
    string res = s;
    for (int i = 0; i < s.size(); i++)
    {
        if (isupper(s[i]))
        {
            res[i] = (s[i] - 'A' + k) % 26 + 'A';
        }
        else
        {
            res[i] = (s[i] - 'a' + k) % 26 + 'a';
        }
    }
    return res;
}

string giaiMa(string s, int k){
    string res = s;
    for (int i = 0; i < s.size(); i++)
    {
        if (isupper(s[i]))
        {
            res[i] = (s[i] - 'A' - k + 26) % 26 + 'A';
        }
        else
        {
            res[i] = (s[i] - 'a' - k + 26) % 26 + 'a';
        }
    }
    return res;
}

// Hàm mã hóa hàng rào
string railFenceEncrypt(string text, int key) {
    vector<string> rail(key);
    int dir = 1, row = 0;

    for (char c : text) {
        rail[row] += c;
        row += dir;
        if (row == 0 || row == key - 1) dir *= -1;
    }

    string result;
    for (const string &r : rail) result += r;
    return result;
}

// Hàm giải mã hàng rào
string railFenceDecrypt(string cipher, int key) {
    vector<int> railLengths(key, 0);
    int dir = 1, row = 0;

    for (int i = 0; i < cipher.size(); i++) {
        railLengths[row]++;
        row += dir;
        if (row == 0 || row == key - 1) dir *= -1;
    }

    vector<string> rail(key);
    int index = 0;
    for (int i = 0; i < key; i++) {
        rail[i] = cipher.substr(index, railLengths[i]);
        index += railLengths[i];
    }

    string result;
    dir = 1, row = 0;
    for (int i = 0; i < cipher.size(); i++) {
        result += rail[row][0];
        rail[row].erase(rail[row].begin());
        row += dir;
        if (row == 0 || row == key - 1) dir *= -1;
    }

    return result;
}

int main() {
    string text;
    int key;

    cout << "Nhập chuỗi cần mã hóa: ";
    getline(cin, text);
    cout << "Nhập số hàng (key): ";
    cin >> key;

    string encrypted = railFenceEncrypt(text, key);
    cout << "Chuỗi sau khi mã hóa: " << encrypted << endl;

    string decrypted = railFenceDecrypt(encrypted, key);
    cout << "Chuỗi sau khi giải mã: " << decrypted << endl;

    return 0;
}