//  dbReader.c
//  SnowCloud
//
//  Created by Christopher Morse on 10/31/12.
//  Copyright(c) 2012 Morse-Code. All rights reserved.
//


#include <my_global.h>
#include <mysql.h>
#include <ctype.h>
#include <errmsg.h>
#include <string.h>


int dbread(MYSQL *conn);

/**************************************************************************************************
/ Establish connection to MySQL database.
/ Parameters: MySQL *conn
/ Return: int 0 if successful; int 1 if error.
**************************************************************************************************/
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
    return 0;
}


char* getLastEntry(MYSQL *conn)
{
        MYSQL_RES *result;
        MYSQL_ROW row;
        char *query = "SELECT MAX(myindex) FROM LATESTQUERY";
        if (mysql_query(conn, query) != 0){
        printf("SQL Error: %d, %s%c", mysql_errno(conn), mysql_error(conn), '\n');
        }
        result = mysql_store_result(conn);
        row  = mysql_fetch_row(result);
        return row[0];
}

/**************************************************************************************************
/ Retrieve entries from database starting with the entry immediately following the most recent entry retrieved during the previeous session.
/ Parameters: MYSQL *conn
/ Return: int 0 if successful; int <> 0 if error.
**************************************************************************************************/
int dbread(MYSQL *conn)
{

    MYSQL_RES *result;
    MYSQL_ROW row;
    int i;
    char *query, *entry;

    char* lastEntry = getLastEntry(conn);
    entry = "SELECT mote, cattribute, dattribute, SNOWDATA.epoch, mytime, myindex "
            "FROM SNOWDATA "
            "WHERE SNOWDATA.myindex > %s "
            "ORDER BY SNOWDATA.myindex";

    asprintf(&query, entry, lastEntry);
    if (mysql_query(conn, query) != 0){
        printf("SQL Error: %d, %s%c", mysql_errno(conn), mysql_error(conn), '\n');
    }

    result = mysql_store_result(conn);
    int num_fields = mysql_num_fields(result);
    while ((row = mysql_fetch_row(result))){
        for(i = 0; i < (num_fields - 3); i++){
            printf("%s\t", row[i] ? row[i] : "NULL");
        }
        printf("%s\n", row[num_fields - 3] ? row[num_fields - 3] : "NULL");
        entry = "INSERT INTO LATESTQUERY(myindex) VALUES('%s')";
        asprintf(&query, entry, row[5]);
    }

    if(mysql_query(conn, query) != 0){
        printf("SQL Error: %d, %s%c", mysql_errno(conn), mysql_error(conn), '\n');
        mysql_query(conn, query);
    }

    mysql_free_result(result);
//    free(entry);

    return 0;
}

int main(int argc, const char *argv[])
{

    MYSQL *conn;
    conn = mysql_init(NULL);

    if (mysql_connection(conn) == 1) {
        exit(1);
    }

    dbread(conn);
    mysql_close(conn);

    exit(0);
}
