//
//  main.c
//  Snow
//
//  Created by Christopher Morse on 10/31/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//


#include <my_global.h>
#include <mysql.h>
#include <ctype.h>
#include <errmsg.h>
#include <string.h>

int main(int argc, const char *argv[]) {
    MYSQL *conn;
    conn = mysql_init(NULL);

    if (mysql_connection(conn) == 1) {
        exit(1);
    }
}
