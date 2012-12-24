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
	char recv[200];
	struct termios newtio,oldtio;    
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
//	printf("%x,%x,%x\n\n",oldtio.c_cflag,oldtio.c_iflag,oldtio.c_oflag);

	tcflush(fd, TCIFLUSH);
	tcsetattr(fd,TCSANOW,&newtio);
	sprintf(send, "SEND COMMAND 156,'P0L%s\%T0'\r",argv[1]);
	write(fd,send,strlen(send));
	printf("set to %s",argv[1]);
	close(fd);        //close the com port
	return 0;
}
