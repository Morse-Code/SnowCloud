//
//  dbWriter.c
//  SnowCloud
//
//  Created by Christopher Morse on 10/31/12.
//  Copyright (c) 2012 Morse-Code. All rights reserved.
//


#include <my_global.h>
#include <mysql.h>
#include <ctype.h>
#include <errmsg.h>
#include <string.h>


int dbwrite(MYSQL *conn, char *mote, char *cattribute, char *dattribute, char *epoch);
void parsetokens(MYSQL *conn);

/**********************************************************************************************
/ Establish connection to MySQL database. Table creation code is commented. Uncomment to initialize new tables..
/ Parameters: MySQL *conn
/ Return: int 0 if successful; int 1 if error.
**********************************************************************************************/
int mysql_connection(MYSQL *conn)
{


    if (conn == NULL) {
        printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
        return 1;
    }

    // Verify connection to propper database.
    if (mysql_real_connect(conn, "localhost", "root", "", "SnowCloud-Test", 0,
    NULL, 0) == NULL) {
        printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
        return 1;
    }

    // Create tables. Really not necessary after the tables have been initialized. Comment out for now.
/*
    mysql_query(conn, "CREATE TABLE SNOWDATA(mote int not null, cattribute int not null, dattribute int not null, epoch int not null, mytime int NOT NULL, myindex int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY)");
    mysql_query(conn, "CREATE TABLE TIMEKEEPER(time int NOT NULL, epoch int NOT NULL, myindex int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY)");
    mysql_query(conn, "CREATE TABLE LATESTQUERY(myindex int unsigned NOT NULL)");
*/

    return 0;
}

/**************************************************************************************************
/ Parses incoming data from stdin into tokens. Tokens are fed as arguments to dbwrite().
/ Parameters: MYSQL connection, conn.
**************************************************************************************************/
void parsetokens(MYSQL *conn)
{

    char *dattribute, *epoch, *mote, *cattribute;
    const char delimiters[] = "mcdr";
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
}

/**************************************************************************************************
/ Write single row tuple to database and corresponding timestamp -epoch tuple to timekeeper db.
/ Parameters: MySQL *conn, char *mote, char *cattribute, char *dattribute, char *epoch
/ Return: int result; The number of characters written to the database.
**************************************************************************************************/
int dbwrite(MYSQL *conn, char *mote, char *cattribute, char *dattribute, char *epoch)
{
    int success;

    if (epoch[0] != '1'){
        return 0;
    }else{
        printf("%s",epoch);
        epoch = &epoch[1];
        printf("%c",'\n');
        printf("%s",epoch);

    }
/*
    char *timedata = "INSERT INTO TIMEKEEPER(time, epoch, myindex) VALUES('%d', '%s', NULL)";
    char *timequery;
    int tstamp = (int)time(NULL);
    asprintf(&timequery, timedata, tstamp, epoch);
    int success = mysql_query(conn, timequery);
    if (success != 0) {
        printf("SQL Error: %d, %s%c", mysql_errno(conn), mysql_error(conn), '\n');
    }*/

    char *stat = "INSERT INTO SNOWDATA(mote, cattribute, dattribute, epoch, mytime, myindex) VALUES('%s', '%s', '%s', '%s', '%d', NULL)";
    char *query;
    int tstamp = (int)time(NULL);
    asprintf(&query, stat, mote, cattribute, dattribute, epoch, tstamp);
    success = mysql_query(conn, query);
    if (success != 0) {
        printf("SQL Error: %d, %s%c", mysql_errno(conn), mysql_error(conn), '\n');
    }
    int result = printf("%s%c", query, '\n');

    fputc('\n', stdout);
    free(query);
    return result;
}

int main(int argc, const char *argv[])
{

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
