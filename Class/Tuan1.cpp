#include <iostream>
#include <string>
#include <locale>

using namespace std;


char encryptChar(char ch, int k) {
    if (isalpha(ch)) { 
        char base = islower(ch) ? 'a' : 'A';
        return (ch - base + k) % 26 + base;
    }
    return ch;  
}

char decryptChar(char ch, int k) {
    if (isalpha(ch)) {
        char base = islower(ch) ? 'a' : 'A';
        return (ch - base - k + 26) % 26 + base;
    }
    return ch;
}

string encryptText(const string &text, int k) {
    string result = text;
    for (size_t i = 0; i < result.length(); i++) {
        result[i] = encryptChar(result[i], k);
    }
    return result;
}

string decryptText(const string &text, int k) {
    string result = text;
    for (size_t i = 0; i < result.length(); i++) {
        result[i] = decryptChar(result[i], k);
    }
    return result;
}

int main() {
    // setlocale(LC_ALL, "");  

    int choice, key, langChoice;
    string text, result;

    // cout << "\n===== CHON NGON NGU =====\n";
    // cout << "1. Tieng Viet\n";
    // cout << "2. Tieng Anh\n";
    // cout << "Chon: ";
    // cin >> langChoice;
    // cin.ignore();
    langChoice=1;

    do {
        cout << "\n===== MA HOA THAY THE =====\n";
        cout << "1. Ma hoa van ban\n";
        cout << "2. Giai ma van ban\n";
        cout << "3. Thoat\n";
        cout << "Chon chuc nang: ";
        cin >> choice;
        cin.ignore();

        if (choice == 1 || choice == 2) {
            cout << "Nhap van ban: ";
            getline(cin, text);

            cout << "Nhap khoa K: ";
            cin >> key;
            cin.ignore();

            if (choice == 1) {
                result = encryptText(text, key);
                cout << "Van ban da ma hoa: " << result << endl;
            } else {
                result = decryptText(text, key);
                cout << "Van ban da giai ma: " << result << endl;
            }
        }

    } while (choice != 3);

    return 0;
}