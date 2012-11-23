//
//  dbWriter.c
//  SnowCloud
//
//  Created by Christopher Morse on 10/31/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//


#include <my_global.h>
#include <mysql.h>
#include <ctype.h>
#include <errmsg.h>
#include <string.h>


int dbwrite(MYSQL *conn, char *mote, char *cattribute, char *dattribute, char *epoch);

int mysql_connection(MYSQL *conn) {

    if (conn == NULL) {
        printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
        return 1;
    }

    // Verify connection to propper database. 
    if (mysql_real_connect(conn, "localhost", "chris", "feb2879", "snowdb", 0, NULL, 0) == NULL) {
        printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
        return 1;
    }
    
    // Create tables. Really not necessary after the tables have been initialized. Comment out for now.
    mysql_query(conn, "CREATE TABLE SNOWDATA(mote int not null, cattribute int not null, dattribute int not null, epoch int not null)");
    mysql_query(conn, "CREATE TABLE TIMEKEEPER(time int not null,epoch int not null)");

    return 0;
}
/*
/ Parses incoming data from stdin into tokens. Tokens are fed as arguments to dbwrite().
/ Parameters: MYSQL connection, conn.
*/
void parsetokens(MYSQL *conn){
    char *dattribute, *epoch, *mote, *cattribute;
    const char delimiters[] = "mcdr";
    char *token;
    size_t nbytes = 100;
    char *line = (char *) malloc(nbytes + 1);
    int bytes_read;
    bytes_read = getline(&line, &nbytes, stdin);
    while (bytes_read != -1){
        mote = strtok(line, delimiters);
        cattribute = strtok(NULL, delimiters);
        dattribute = strtok(NULL, delimiters);
        epoch = strtok(NULL, delimiters);
        int success = dbwrite(conn, mote, cattribute, dattribute, epoch);
        printf("Characters printed: %d\n", success);
        bytes_read = getline(&line, &nbytes, stdin);
    }
//
}


int dbwrite(MYSQL *conn, char *mote, char *cattribute, char *dattribute, char *epoch) {

    if (epoch[0] != '1'){
        return 0;
    }else{
        printf("%s",epoch);
        epoch = &epoch[1];
        printf("%c",'\n');
        printf("%s",epoch);

    }

    char *stat = "INSERT INTO SNOWDATA(mote, cattribute, dattribute, epoch) VALUES('%s', '%s', '%s', '%s')";
    char *query;
    asprintf(&query, stat, mote, cattribute, dattribute, epoch);
    int success = mysql_query(conn, query);
    if (success != 0) {
        printf("SQL Error: %d%c", mysql_errno(conn), '\n');
    }
    int result = printf("%s%c", query, '\n');

    char *timedata = "INSERT INTO TIMEKEEPER( time, epoch) VALUES('%d', '%s')";
    char *timequery;
    int tstamp = (int)time(NULL);
    asprintf(&timequery, timedata, tstamp, epoch);
    success = mysql_query(conn, timequery);

    fputc('\n', stdout);
    free(query);
    return result;

}


int main(int argc, const char *argv[]) {
    MYSQL *conn;
    conn = mysql_init(NULL);

    if (mysql_connection(conn) == 1) {
        exit(1);
    }

    //TODO Function to test existence of Tables. If found, return success, else create tables. 

    parsetokens(conn);
    mysql_close(conn);

    exit(0);
}
