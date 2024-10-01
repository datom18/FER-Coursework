#include <iostream>
#include <pthread.h>
#include <unistd.h>
#define BR_CITACA 10
#define BR_PISACA 4
#define BR_BRISACA 2

using namespace std;

template <class T> class List {
   
   template <class X> struct ListElement {
      X data;
      ListElement<X> *next;
   };

   ListElement<T> *head = nullptr;

public:

    bool append(T data) {
        ListElement<T> *newElement = new ListElement<T>;
        if (newElement == nullptr)
            return false;
        newElement->data = data;
        newElement->next = nullptr;

        if (!head) {
            head = newElement;
        } 
        else {
            ListElement<T> *p;
            for (p = head; p->next; p = p->next)
            ; 
            p->next = newElement;
        }

        return true;
    }
   
    bool remove(int index) {

        ListElement<T> **p = &head;
        for (int i = 0; *p != nullptr && i < index; i++) {
            p = &((*p)->next);
        }

        if (*p == nullptr) {
            return false;
        }

        ListElement<T> *tmp = *p;
        *p = (*p)->next;
        delete tmp;
        return true;
    }

    T get(int index) {

        ListElement<T> *p = head;
        for (int i = 0; p != nullptr && i < index; i++, p = p->next) {
            ;
        }

        if (p == nullptr) {
            return -1;
        }

        return p->data;
    }


    int size() {
        int c = 0;
        for (ListElement<T> *p = head; p; p = p->next) {
            c++;
        }
        return c;
    }

    void print() {
        for (ListElement<T> *p = head; p; p = p->next) {
            cout << p->data << " ";
        }
        cout << endl;
    }

};

List<int> l;

pthread_mutex_t monitor;
pthread_cond_t citac_cond, pisac_cond, brisac_cond;
int waiting_citac, waiting_pisac, waiting_brisac = 0;
int citac_active, pisac_active, brisac_active = 0;

void printStatus() {
    printf("Aktivni: Citaci=%d, Pisaci=%d, Brisaci=%d\n", citac_active, pisac_active, brisac_active);
    printf("Lista: ");
    l.print();
    cout << endl;
}


void* citac_thread(void* rbr) {

    int ind = *((int *) rbr);
    while (1) {
        
        int pos = rand() % l.size();

        pthread_mutex_lock(&monitor);
        
        printf("Citac (%d) zeli citati %d. element liste.\n", ind, pos+1);
        printStatus();

        waiting_citac++;

        while (brisac_active + waiting_brisac > 0) {
            pthread_cond_wait(&citac_cond, &monitor);
        }

        citac_active++;
        waiting_citac--;

        int r = l.get(pos);
        printf("Citac (%d) cita %d. element liste (vrijednost=%d).\n", ind, pos+1, r);
        printStatus();

        pthread_mutex_unlock(&monitor);
        
        sleep(5);


        pthread_mutex_lock(&monitor);

        citac_active--;

        if (citac_active == 0 && waiting_brisac > 0) {
            pthread_cond_signal(&brisac_cond);
        }

        printf("Citac (%d) vise ne koristi listu.\n", ind);
        printStatus();

        pthread_mutex_unlock(&monitor);

        sleep(5);

    }

}


void* pisac_thread(void* rbr) {

    int ind = *((int *) rbr);
    while (1) {

        pthread_mutex_lock(&monitor);

        int n = rand() % 100 + 1;
        printf("Pisac (%d) zeli dodati %d u listu.\n", ind, n);
        printStatus();

        waiting_pisac++;
        while (pisac_active == 1 || brisac_active == 1 || waiting_brisac > 0) {
            pthread_cond_wait(&pisac_cond, &monitor);
        }
        waiting_pisac--;
        pisac_active = 1;

        l.append(n);
        printf("Pisac (%d) zapisuje vrijednost %d u listu.\n", ind, n);
        printStatus();

        pthread_mutex_unlock(&monitor);


        pthread_mutex_lock(&monitor);

        pisac_active = 0;

        if (waiting_brisac > 0) {
            pthread_cond_signal(&brisac_cond);
        }
        else if (waiting_pisac > 0) {
            pthread_cond_signal(&pisac_cond);
        }
        else {
            pthread_cond_broadcast(&citac_cond);
        }

        pthread_mutex_unlock(&monitor);


        sleep(4);
    }

}

void* brisac_thread(void* rbr) {

    int ind = *((int *) rbr);
    while (1) {

        pthread_mutex_lock(&monitor);

        int d = rand() % l.size();

        printf("Brisac (%d) zeli obrisati %d. element iz liste.\n", ind, d+1);
        printStatus();


        waiting_brisac++;
        while (pisac_active==1 || brisac_active==1 || citac_active > 0) {
            pthread_cond_wait(&brisac_cond, &monitor);
        }

        waiting_brisac--;
        brisac_active = 1;

        int val = l.get(d);
        l.remove(d);
        printf("Brisac (%d) brise %d. element liste (vrijednost=%d).\n", ind, d+1, val);
        printStatus();

        pthread_mutex_unlock(&monitor);
    

        pthread_mutex_lock(&monitor);

        brisac_active = 0;
        if (waiting_brisac > 0) {
            pthread_cond_signal(&brisac_cond);
        }    
        else if (waiting_pisac > 0) {
            pthread_cond_signal(&pisac_cond);
        }
        else {
            pthread_cond_broadcast(&citac_cond);
        }
    
        pthread_mutex_unlock(&monitor);
    

        sleep(4);
    }

}



int main() {

    pthread_mutex_init(&monitor, nullptr);
    pthread_cond_init(&citac_cond, nullptr);
    pthread_cond_init(&pisac_cond, nullptr);
    pthread_cond_init(&brisac_cond, nullptr);

    pthread_t citac[BR_CITACA], pisac[BR_PISACA], brisac[BR_BRISACA];
    
    for (int i = 0; i < BR_PISACA; i++) {
        int *rbr = (int*)malloc(sizeof(int));
        *rbr = i;
        pthread_create(&pisac[i], nullptr, pisac_thread, (void*)rbr);
        //sleep(2);
    }

    sleep(4);

    for (int i = 0; i < BR_CITACA; i++) {
        int *rbr = (int*)malloc(sizeof(int));
        *rbr = i;
        pthread_create(&citac[i], nullptr, citac_thread, (void*)rbr);
        //sleep(2);
    }


    for (int i = 0; i < BR_BRISACA; i++) {
        int *rbr = (int*)malloc(sizeof(int));
        *rbr = i;
        pthread_create(&brisac[i], nullptr, brisac_thread, (void*)rbr);
        //sleep(2);
    }    



    for (int i = 0; i < 3; i++) {
        pthread_join(citac[i], nullptr);
    }

    for (int i = 0; i < 3; i++) {
        pthread_join(pisac[i], nullptr);
    }

    for (int i = 0; i < 3; i++) {
        pthread_join(brisac[i], nullptr);
    }

    pthread_mutex_destroy(&monitor);
    pthread_cond_destroy(&citac_cond);
    pthread_cond_destroy(&pisac_cond);
    pthread_cond_destroy(&brisac_cond);

    return 0;
}