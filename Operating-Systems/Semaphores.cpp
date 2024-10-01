#include <iostream>
#include <ctime>
#include <vector>
#include <pthread.h>
#include <unistd.h>
#include <semaphore.h>

#define BUD 4 // br. ulaznih dretvi
#define BRD 6 // br. radnih dretvi
#define BID 3 // br. izlaznih dretvi
#define MS_SIZE 8 // velicina meduspremnika

using namespace std;

class Queue {

private: 
    vector<char> arr;
    int size;
    int front;
    int rear;

public:

    Queue(int size): size(size), front(0), rear(0) {
        
        arr.resize(size);
        for (int i = 0; i < size; ++i) {
            arr[i] = '-';
        }
    }
    
    bool isEmpty() {
        for (int i = 0; i < size; i++) {
            if (arr[i] != '-')
                return false;
        }
        return true;
    }    

    bool isFull() {
        for (int i = 0; i < size; i++) {
            if (arr[i] == '-')
                return false;
        }
        return true;
    }

    void enqueue(char value) {
        
        if (arr[front] == '-') {
            arr[front] = value;
            front = (front + 1) % size;
        }
        else {
            arr[front] = value;
            front = (front + 1) % size;
            rear = (rear + 1) % size;
        }

    }

    char dequeue() {

        if (isEmpty()) {
            return '-';
        }

        char c = arr[rear];
        arr[rear] = '-';
        rear = (rear + 1) % size;
        
        return c;
    }

    int count() {
        int c = 0;
        for (int i = 0; i < size; i++) {
            if (arr[i] != '-')
                c++;
        }
        return c;
    }


    void display() {
        for (int i = 0; i < size; i++) {
            cout << arr[i];
        }
        cout << "  ";
    }

};



vector<Queue> ums(BRD, Queue(MS_SIZE));
vector<Queue> ims(BID, Queue(MS_SIZE));


void printMS() {
    cout << "UMS[]: ";
    for (int i = 0; i < ums.size(); i++) {
        ums[i].display();
    }
    cout << endl;
    cout << "IMS[]: ";
    for (int i = 0; i < ims.size(); i++) {
        ims[i].display();
    }
    cout << endl << endl;
}


char getRandomChar() {
    int r = rand() % 52;
    char base = (r < 26) ? 'A' : 'a';
    return (char) (base + r % 26);
}

int getRandomIndex(int size) {
    return rand() % size;
}

char processChar(char c) {
    if (islower(c)) {
        return toupper(c);
    }
    else if (isupper(c)) {
        return tolower(c);
    }
    else
        return c;
}


sem_t ums_bsem[BRD];
sem_t ums_osem[BRD];

sem_t ims_bsem[BID];
sem_t ims_osem[BID];

sem_t print_bsem;

int ims_el_num[BID] = {0};
bool ims_added[BID] = {false};
char ims_prev_char[BID] = {'0'};


void* ulaznaDretva(void* rbr) {

    int ind = *((int *) rbr);
    while (true) {
        
        int t = rand() % 3 + 4; 
        sleep(t);

        char c = getRandomChar();
        int ums_rand = getRandomIndex(BRD);
    
        sem_wait(&ums_bsem[ums_rand]);

        sem_wait(&print_bsem);

        ums[ums_rand].enqueue(c);

        if (!ums[ums_rand].isFull()) {
            sem_post(&ums_osem[ums_rand]);
        }
        sem_post(&ums_bsem[ums_rand]);

        printf("U%d: dohvati_ulaz(%d)=>'%c'; obradi_ulaz('%c')=>%d; '%c' => UMS[%d]\n", ind, ind, c, c, ums_rand, c, ums_rand);   
        printMS();

        sem_post(&print_bsem); 

    }
}

void* radnaDretva(void* rbr) {
    
    int ind = *((int *) rbr);
    while (true) {
        
        int t = rand() % 4 + 2;
        sleep(t);

        sem_wait(&ums_osem[ind]);
        sem_wait(&ums_bsem[ind]);
        
        sem_wait(&print_bsem);

        char c = ums[ind].dequeue();

        sem_post(&ums_bsem[ind]);


        char processed_c = processChar(c);
        int ims_rand = getRandomIndex(BID);

        sem_wait(&ims_bsem[ims_rand]);


        ims[ims_rand].enqueue(processed_c);

        if (!ims[ims_rand].isFull()) {
            sem_post(&ims_osem[ims_rand]);
        }
        sem_post(&ims_bsem[ims_rand]);

        printf("R%d: uzima '%c' iz UMS[%d]; obradi('%c')=>'%c'; '%c' => IMS[%d]\n", ind, c, ind, c, processed_c, processed_c, ims_rand);
        printMS();

        sem_post(&print_bsem);
        
    }
}

void* izlaznaDretva(void* rbr) {

    int ind = *((int *) rbr);
    while (true) {
        
        int t = rand() % 4 + 2;
        sleep(t);

        sem_wait(&ims_bsem[ind]);
        
        sem_wait(&print_bsem);

        char val = '0';
        if (ims[ind].count() > ims_el_num[ind]) {
            val = ims[ind].dequeue();
            ims_prev_char[ind] = val;
            ims_el_num[ind] = ims[ind].count();
            ims_added[ind] = false;
        }
        if (ims[ind].count() <= ims_el_num[ind]) {
            val = ims_prev_char[ind];
        }

        sem_post(&ims_bsem[ind]);
        
        printf("I%d: Saljem vrijednost iz IMS[%d] na izlaz: '%c'\n", ind, ind, val);
        printMS();
        
        sem_post(&print_bsem);

    }
}


int main() {

    cout << "Broj ulaznih dretvi: " << BUD << endl;
    cout << "Broj radnih dretvi: " << BRD << endl;
    cout << "Broj izlaznih dretvi: " << BID << endl << endl;


    srand(time(NULL));

    for (int i = 0; i < BRD; i++) {        
        sem_init(&ums_bsem[i], 0, 1);
    }

    for (int i = 0; i < BRD; i++) {
        sem_init(&ums_osem[i], 0, 0);
    }

    for (int i = 0; i < BID; i++) {
        sem_init(&ims_bsem[i], 0, 1);
    }

    for (int i = 0; i < BID; i++) {
        sem_init(&ims_osem[i], 0, 0);
    }

    sem_init(&print_bsem, 0, 1);

    pthread_t ulazna_thread[BUD], radna_thread[BRD], izlazna_thread[BID];

    for (int i = 0; i < BUD; i++) {
        int *rbr = (int*)malloc(sizeof(int));
        *rbr = i;
        pthread_create(&ulazna_thread[i], nullptr, ulaznaDretva, (void*)rbr);
        //sleep(2);
    }

    sleep(20);

    for (int i = 0; i < BRD; i++) {
        int *rbr = (int*)malloc(sizeof(int));
        *rbr = i;
        pthread_create(&radna_thread[i], nullptr, radnaDretva, (void*)rbr);
        //sleep(2);
    }

    sleep(5);

    for (int i = 0; i < BID; i++) {
        int *rbr = (int*)malloc(sizeof(int));
        *rbr = i;
        pthread_create(&izlazna_thread[i], nullptr, izlaznaDretva, (void*)rbr);
        //sleep(2);
    }

    
    for (int i = 0; i < BRD; i++) {
        pthread_join(ulazna_thread[i], nullptr);
    }    

    for (int i = 0; i < BRD; i++) {
        pthread_join(radna_thread[i], nullptr);
    }

    for (int i = 0; i < BRD; i++) {
        pthread_join(izlazna_thread[i], nullptr);
    }


    for (int i = 0; i < BRD; ++i) {
        sem_destroy(&ums_bsem[i]);
    }
    
    for (int i = 0; i < BRD; ++i) {
        sem_destroy(&ums_osem[i]);
    }

    for (int i = 0; i < BID; ++i) {
        sem_destroy(&ims_bsem[i]);
    }

    for (int i = 0; i < BID; ++i) {
        sem_destroy(&ims_osem[i]);
    }

    sem_destroy(&print_bsem);

    return 0;
}