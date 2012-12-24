#include <termios.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/signal.h>
#include <sys/types.h>

int main(int argc, char *argv[]) {
	int fd;
	char devicename[20];
	char send[20];
	struct termios newtio;    
	sprintf(devicename,"/dev/ttyS0");
	fd = open(devicename, O_RDWR | O_NOCTTY | O_NONBLOCK);
	if (fd < 0) 	{
		perror(devicename);
		return -1;
	}
	newtio.c_cflag = 0x8bf;
	newtio.c_iflag = 0x1;
	newtio.c_oflag = 0x0;
	newtio.c_lflag = 0x0;       //ICANON;
	newtio.c_cc[VMIN]=1;
	newtio.c_cc[VTIME]=0;
//	tcgetattr(fd,&oldtio);
	tcflush(fd, TCIFLUSH);
	tcsetattr(fd,TCSANOW,&newtio);
	if(argv[1][1] == '\0') {
		sprintf(send, "pulse[6,10]\r");
		write(fd,send,strlen(send));
		sprintf(send, "pulse[6,1%c]\r",argv[1][0]);
		sleep(1);
		write(fd,send,strlen(send));
	}
	else {
		sprintf(send, "pulse[6,1%c]\r",argv[1][0]);
		write(fd,send,strlen(send));
		sprintf(send, "pulse[6,1%c]\r",argv[1][1]);
		sleep(1);
		write(fd,send,strlen(send));
	}
	sprintf(send, "pulse[6,53]\r");
	sleep(1);
	write(fd,send,strlen(send));
	close(fd);        //close the com port
	return 0;
}
