
//#include <limits>
//#include <cstdint>
#include <sys/ioctl.h>
#include <linux/cdrom.h>
#include <fcntl.h>
#include <iostream>
#include <unistd.h>
using namespace std;

int main(int argc,char **argv)
{
    int cdrom=0;
    if ((cdrom = open(argv[1],O_RDONLY | O_NONBLOCK)) < 0) {
        cout<<"Unable to open device. Provide a device name (/dev/sr0, /dev/cdrom) as a parameter."<<endl;
        exit(-1);
    }
int result=ioctl(cdrom, CDROM_DRIVE_STATUS, 0);
cout<<"CDROM status of "<<argv[1]<<" : ";
switch(result) {
  case CDS_NO_INFO: 
    cout<<"No info"<<endl;
   break;
  case CDS_NO_DISC: 
    cout<<"No disc"<<endl;
   break;
  case CDS_TRAY_OPEN: 
   
    cout<<"Tray open"<<endl;
    break;
  case CDS_DRIVE_NOT_READY: 
    cout<<"Not ready"<<endl;
     break;
  case CDS_DISC_OK: 
    cout<<"Disc ok"<<endl;
     break;
  default:  /*error*/ 
    cout<<"Error"<<endl;
    }
close(cdrom);
exit(result);

}
