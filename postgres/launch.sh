#!/bin/bash

psql -d $POSTGRES_DB -f /postgres/initDB/create.sql