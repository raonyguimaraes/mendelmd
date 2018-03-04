#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <errno.h>

int main() {
    char* fName = "/storage3/1000genomes/ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf";
    //
    struct stat sb;
    long cntr = 0;
    int fd, lineLen;
    char *data;
    char *line;
    // map the file
    fd = open(fName, O_RDONLY);
    fstat(fd, &sb);
    //// int pageSize;
    //// pageSize = getpagesize();
    //// data = mmap((caddr_t)0, pageSize, PROT_READ, MAP_PRIVATE, fd, pageSize);
    data = mmap((caddr_t)0, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    line = data;
    // get lines
    while(cntr < sb.st_size) {
        lineLen = 0;
        line = data;
        // find the next line
        while(*data != '\n' && cntr < sb.st_size) {
            data++;
            cntr++;
            lineLen++;
        }
        /***** PROCESS LINE *****/
        // ... processLine(line, lineLen);
    }
    return 0;
}