#include<bits/stdc++.h> 
using namespace std;
#define int long long
#define Y cout<<"YES"<<endl
#define N cout<<"NO"<<endl
#define D cout<<"DEBUG"<<endl

void reverse(int* a,int i,int j){
    while(i<j){
        int tmp = a[i];
        a[i] = a[j];
        a[j] = tmp;
        i++;
        j--;
    }
}

void rotate(int* a, int n, int m){
    int i = 0;
    int j = m-1;
    reverse(a,i,j);

    i = 0;
    j = n-1;
    reverse(a,i,j);

    i = n;
    j = m-1;
    reverse(a,i,j);

    return;

}


int32_t main(){
    int m;
    cin>>m;
    int a[m];
    for(int i=0;i<m;i++)cin>>a[i];
    
    int n;cin>>n;

    rotate(a,n,m);

    for(int i=0;i<m;i++)cout<<a[i]<<" ";
}

 
 
 
 
 
 
























