
#include "base.c"

int main()
{
	T[P] += 8;
	U();
	while (T[P] != 0) {
		P++;
		T[P] += 4;
		U();
		while (T[P] != 0) {
			P++;
			T[P] += 2;
			P++;
			T[P] += 3;
			P++;
			T[P] += 3;
			P++;
			T[P]++;
			P -= 4;
			T[P]--;
			U();
		}
		P++;
		T[P]++;
		P++;
		T[P]++;
		P++;
		T[P]--;
		P += 2;
		T[P]++;
		U();
		while (T[P] != 0) {
			P--;
			U();
		}
		P--;
		T[P]--;
		U();
	}
	P += 2;
	O();
	P++;
	T[P] -= 3;
	O();
	T[P] += 7;
	O();
	O();
	T[P] += 3;
	O();
	P += 2;
	O();
	P--;
	T[P]--;
	O();
	P--;
	O();
	T[P] += 3;
	O();
	T[P] -= 6;
	O();
	T[P] -= 8;
	O();
	P += 2;
	T[P]++;
	O();
	P++;
	T[P] += 2;
	O();
}
