//
//  dbReader.c
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
    
    return 0;
}

int main(int argc, const char *argv[]) {
    MYSQL *conn;
    conn = mysql_init(NULL);

    if (mysql_connection(conn) == 1) {
        exit(1);
    }



    mysql_close(conn);

    exit(0);
}
