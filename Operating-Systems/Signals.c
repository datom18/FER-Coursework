#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

int t_p = 0;
int k_z[4] = {0, 0, 0, 0};

int vrh = 0;
int stog[128];

void push(int x) {
	vrh++;
	stog[vrh] = x;
}

int pop() {
	return stog[vrh--];
}

void ispis_stog() {
	
	printf("stog: ");
	if (vrh > 0) {
			for (int i = 1; i <= vrh; i++) {
			printf("%d,reg[%d] ", stog[i], stog[i]);
		}
		printf("\n");
	}	
	else { printf("-\n"); }
}

void ispis() {
	printf("T_P=%d, K_Z=", t_p);
	for (int i = 0; i < 4; i++) printf("%d", k_z[i]);
	printf(", ");
	ispis_stog();
	printf("\n");
}

void obradi_dogadjaj(int sig);
void obradi_signal1(int sig);
void obradi_signal2(int sig);
void obradi_signal3(int sig);
void obradi_signal4(int sig);

int prioritet;

int main() {

	struct sigaction act;

	act.sa_handler = obradi_dogadjaj;
	act.sa_flags = SA_NODEFER;
	
	sigaction(SIGINT, &act, NULL);

	printf("Glavni program (pid: %ld) je počeo s radom.\n", (long) getpid());
	ispis();
	int i = 1;
	while (1) {
		printf("Glavni program (pid: %ld)... (%d)\n", (long)getpid(), i++);
		sleep(2);
	}

}

void obradi_dogadjaj(int sig) {

	printf("Poslan signal, odabrati prioritet signala:\n");
	scanf("%d", &prioritet);

	k_z[prioritet-1] = 1;

	if (k_z[0] != 0 || k_z[1] != 0 || k_z[2] != 0 || k_z[3] != 0) {
		if (k_z[3] != 0) obradi_signal4(SIGINT);
		if (k_z[2] != 0) obradi_signal3(SIGINT);
		if (k_z[1] != 0) obradi_signal2(SIGINT);
		if (k_z[0] != 0) obradi_signal1(SIGINT);
	}

}

void obradi_signal4(int sig) {

	printf("Dogodio se prekid razine 4.\n");
	ispis();
	printf("Pocetak obrade signala prioriteta 4.\n");
	push(t_p);
	t_p = 4;
	k_z[t_p-1] = 0;
	ispis();
	for (int i = 1; i <= 5; i++) {
		printf("Obrada signala prioriteta 4: %d/5\n", i);
		sleep(2);
	}
	printf("Kraj obrade signala prioriteta 4\n");
	t_p = pop();
	ispis();
}

void obradi_signal3(int sig) {

	if (t_p < 3) {
		printf("Dogodio se prekid razine 3.\n");
		ispis();
		printf("Pocetak obrade signala prioriteta 3.\n");
		push(t_p);
		t_p = 3;
		k_z[t_p-1] = 0;
		ispis();
		for (int i = 1; i <= 5; i++) {
			printf("Obrada signala prioriteta 3: %d/5\n", i);
			sleep(2);
		}
		printf("Kraj obrade signala prioriteta 3\n");
		t_p = pop();
		ispis();
	}
}

void obradi_signal2(int sig) {

	if (t_p < 2) {
		printf("Dogodio se prekid razine 2.\n");
		ispis();
		printf("Pocetak obrade signala prioriteta 2.\n");
		push(t_p);
		t_p = 2;
		k_z[t_p-1] = 0;
		ispis();
		for (int i = 1; i <= 5; i++) {
			printf("Obrada signala prioriteta 2: %d/5\n", i);
			sleep(2);
		}
		printf("Kraj obrade signala prioriteta 2\n");
		t_p = pop();
		ispis();
	}
}

void obradi_signal1(int sig) {

	if (t_p < 1) {
		printf("Dogodio se prekid razine 1.\n");
		ispis();
		printf("Pocetak obrade signala prioriteta 1.\n");
		push(t_p);
		t_p = 1;
		k_z[t_p-1] = 0;
		ispis();
		for (int i = 1; i <= 5; i++) {
			printf("Obrada signala prioriteta 1: %d/5\n", i);
			sleep(2);
		}
		printf("Kraj obrade signala prioriteta 1\n");
		t_p = pop();
		ispis();
	}
}